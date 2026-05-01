"""
Order routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app.middleware.auth import jwt_required_custom, admin_required, get_current_user
from app.utils.validators import validate_required_fields
from app.utils.payment_helper import payment_helper

bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@bp.route('', methods=['GET'])
@jwt_required_custom
def get_orders():
    """Get user's orders or all orders (admin)"""
    try:
        user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if user.is_admin():
            # Admin can see all orders
            query = Order.query
        else:
            # Users see only their orders
            query = Order.query.filter_by(user_id=user.id)
        
        # Apply filters
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        # Order by most recent first
        query = query.order_by(Order.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'orders': [order.to_dict() for order in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch orders', 'message': str(e)}), 500

@bp.route('/<int:order_id>', methods=['GET'])
@jwt_required_custom
def get_order(order_id):
    """Get single order"""
    try:
        user = get_current_user()
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Check authorization
        if not user.is_admin() and order.user_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({'order': order.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch order', 'message': str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required_custom
def create_order():
    """Create a new order from cart"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['shipping_address', 'shipping_city', 'shipping_state', 
                          'shipping_zip', 'shipping_country', 'payment_method']
        is_valid, error = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Get cart items
        cart_items = Cart.query.filter_by(user_id=user.id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total and validate stock
        total_amount = 0
        for cart_item in cart_items:
            product = cart_item.product
            
            if not product.is_active:
                return jsonify({'error': f'Product {product.name} is no longer available'}), 400
            
            if product.stock < cart_item.quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
            
            total_amount += product.price * cart_item.quantity
        
        # Process payment if using Stripe
        payment_id = None
        payment_status = 'pending'
        
        if data['payment_method'] == 'stripe' and data.get('payment_intent_id'):
            payment_result = payment_helper.confirm_payment(data['payment_intent_id'])
            
            if payment_result['success'] and payment_result['status'] == 'succeeded':
                payment_id = data['payment_intent_id']
                payment_status = 'paid'
            else:
                return jsonify({'error': 'Payment failed', 'details': payment_result.get('error')}), 400
        
        # Create order
        order = Order(
            user_id=user.id,
            total_amount=total_amount,
            status='pending',
            payment_status=payment_status,
            payment_method=data['payment_method'],
            payment_id=payment_id,
            shipping_address=data['shipping_address'],
            shipping_city=data['shipping_city'],
            shipping_state=data['shipping_state'],
            shipping_zip=data['shipping_zip'],
            shipping_country=data['shipping_country'],
            shipping_phone=data.get('shipping_phone'),
            notes=data.get('notes')
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and update stock
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
        
        # Clear cart
        Cart.query.filter_by(user_id=user.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order', 'message': str(e)}), 500

@bp.route('/<int:order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """Update order status (Admin only)"""
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
            order.status = data['status']
        
        if 'payment_status' in data:
            valid_payment_statuses = ['pending', 'paid', 'failed']
            if data['payment_status'] not in valid_payment_statuses:
                return jsonify({'error': f'Invalid payment status. Must be one of: {", ".join(valid_payment_statuses)}'}), 400
            order.payment_status = data['payment_status']
        
        if 'notes' in data:
            order.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update order', 'message': str(e)}), 500

@bp.route('/create-payment-intent', methods=['POST'])
@jwt_required_custom
def create_payment_intent():
    """Create a Stripe payment intent"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data.get('amount'):
            return jsonify({'error': 'Amount is required'}), 400
        
        result = payment_helper.create_payment_intent(
            amount=float(data['amount']),
            metadata={
                'user_id': user.id,
                'user_email': user.email
            }
        )
        
        if result['success']:
            return jsonify({
                'client_secret': result['client_secret'],
                'payment_intent_id': result['payment_intent_id']
            }), 200
        else:
            return jsonify({'error': 'Failed to create payment intent', 'details': result.get('error')}), 500
    except Exception as e:
        return jsonify({'error': 'Payment processing failed', 'message': str(e)}), 500
