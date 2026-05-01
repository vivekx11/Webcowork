"""
Admin routes for analytics and management
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract
from app import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.middleware.auth import admin_required
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/analytics', methods=['GET'])
@admin_required
def get_analytics():
    """Get dashboard analytics"""
    try:
        # Total users
        total_users = User.query.filter_by(role='user').count()
        
        # Total products
        total_products = Product.query.count()
        active_products = Product.query.filter_by(is_active=True).count()
        
        # Total orders
        total_orders = Order.query.count()
        pending_orders = Order.query.filter_by(status='pending').count()
        
        # Total sales
        total_sales = db.session.query(func.sum(Order.total_amount)).filter(
            Order.payment_status == 'paid'
        ).scalar() or 0
        
        # Recent orders (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_orders = Order.query.filter(Order.created_at >= thirty_days_ago).count()
        
        # Recent sales (last 30 days)
        recent_sales = db.session.query(func.sum(Order.total_amount)).filter(
            Order.created_at >= thirty_days_ago,
            Order.payment_status == 'paid'
        ).scalar() or 0
        
        # Top selling products
        top_products = db.session.query(
            Product.id,
            Product.name,
            Product.image_url,
            func.sum(OrderItem.quantity).label('total_sold'),
            func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
        ).join(OrderItem).join(Order).filter(
            Order.payment_status == 'paid'
        ).group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
        
        top_products_data = [{
            'id': p.id,
            'name': p.name,
            'image_url': p.image_url,
            'total_sold': p.total_sold,
            'total_revenue': float(p.total_revenue)
        } for p in top_products]
        
        # Low stock products
        low_stock_products = Product.query.filter(
            Product.stock < 10,
            Product.is_active == True
        ).order_by(Product.stock.asc()).limit(10).all()
        
        return jsonify({
            'total_users': total_users,
            'total_products': total_products,
            'active_products': active_products,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'total_sales': float(total_sales),
            'recent_orders': recent_orders,
            'recent_sales': float(recent_sales),
            'top_products': top_products_data,
            'low_stock_products': [p.to_dict() for p in low_stock_products]
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch analytics', 'message': str(e)}), 500

@bp.route('/sales', methods=['GET'])
@admin_required
def get_sales_data():
    """Get sales data for charts"""
    try:
        period = request.args.get('period', 'month')  # day, week, month, year
        
        if period == 'day':
            # Last 24 hours
            start_date = datetime.utcnow() - timedelta(days=1)
            group_by = func.strftime('%H:00', Order.created_at)
        elif period == 'week':
            # Last 7 days
            start_date = datetime.utcnow() - timedelta(days=7)
            group_by = func.date(Order.created_at)
        elif period == 'year':
            # Last 12 months
            start_date = datetime.utcnow() - timedelta(days=365)
            group_by = func.strftime('%Y-%m', Order.created_at)
        else:  # month
            # Last 30 days
            start_date = datetime.utcnow() - timedelta(days=30)
            group_by = func.date(Order.created_at)
        
        # Sales data
        sales_data = db.session.query(
            group_by.label('period'),
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('total_sales')
        ).filter(
            Order.created_at >= start_date,
            Order.payment_status == 'paid'
        ).group_by('period').order_by('period').all()
        
        sales_chart_data = [{
            'period': str(s.period),
            'order_count': s.order_count,
            'total_sales': float(s.total_sales) if s.total_sales else 0
        } for s in sales_data]
        
        # Order status distribution
        status_data = db.session.query(
            Order.status,
            func.count(Order.id).label('count')
        ).group_by(Order.status).all()
        
        status_chart_data = [{
            'status': s.status,
            'count': s.count
        } for s in status_data]
        
        return jsonify({
            'sales_data': sales_chart_data,
            'status_data': status_chart_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch sales data', 'message': str(e)}), 500

@bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = User.query.filter_by(role='user')
        
        # Search
        search = request.args.get('search')
        if search:
            query = query.filter(
                (User.email.ilike(f'%{search}%')) |
                (User.first_name.ilike(f'%{search}%')) |
                (User.last_name.ilike(f'%{search}%'))
            )
        
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'message': str(e)}), 500

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (Admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.is_admin():
            return jsonify({'error': 'Cannot delete admin user'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user', 'message': str(e)}), 500
