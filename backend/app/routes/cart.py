"""
Cart routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.cart import Cart
from app.models.product import Product
from app.middleware.auth import jwt_required_custom, get_current_user

bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@bp.route('', methods=['GET'])
@jwt_required_custom
def get_cart():
    """Get user's cart"""
    try:
        user = get_current_user()
        cart_items = Cart.query.filter_by(user_id=user.id).all()
        
        total = sum(item.product.price * item.quantity for item in cart_items if item.product)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total': total,
            'item_count': len(cart_items)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch cart', 'message': str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required_custom
def add_to_cart():
    """Add item to cart"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data.get('product_id'):
            return jsonify({'error': 'Product ID is required'}), 400
        
        # Check if product exists
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check stock
        quantity = data.get('quantity', 1)
        if product.stock < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Check if item already in cart
        cart_item = Cart.query.filter_by(
            user_id=user.id,
            product_id=data['product_id']
        ).first()
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                return jsonify({'error': 'Insufficient stock'}), 400
        else:
            # Create new cart item
            cart_item = Cart(
                user_id=user.id,
                product_id=data['product_id'],
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to cart',
            'cart_item': cart_item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add to cart', 'message': str(e)}), 500

@bp.route('/<int:cart_id>', methods=['PUT'])
@jwt_required_custom
def update_cart_item(cart_id):
    """Update cart item quantity"""
    try:
        user = get_current_user()
        cart_item = Cart.query.filter_by(id=cart_id, user_id=user.id).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        data = request.get_json()
        quantity = data.get('quantity', 1)
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
        
        # Check stock
        if cart_item.product.stock < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'message': 'Cart updated',
            'cart_item': cart_item.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update cart', 'message': str(e)}), 500

@bp.route('/<int:cart_id>', methods=['DELETE'])
@jwt_required_custom
def remove_from_cart(cart_id):
    """Remove item from cart"""
    try:
        user = get_current_user()
        cart_item = Cart.query.filter_by(id=cart_id, user_id=user.id).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from cart'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove from cart', 'message': str(e)}), 500

@bp.route('/clear', methods=['DELETE'])
@jwt_required_custom
def clear_cart():
    """Clear all items from cart"""
    try:
        user = get_current_user()
        Cart.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        
        return jsonify({'message': 'Cart cleared'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to clear cart', 'message': str(e)}), 500
