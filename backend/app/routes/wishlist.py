"""
Wishlist routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.wishlist import Wishlist
from app.models.product import Product
from app.middleware.auth import jwt_required_custom, get_current_user

bp = Blueprint('wishlist', __name__, url_prefix='/api/wishlist')

@bp.route('', methods=['GET'])
@jwt_required_custom
def get_wishlist():
    """Get user's wishlist"""
    try:
        user = get_current_user()
        wishlist_items = Wishlist.query.filter_by(user_id=user.id).all()
        
        return jsonify({
            'wishlist_items': [item.to_dict() for item in wishlist_items],
            'item_count': len(wishlist_items)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch wishlist', 'message': str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required_custom
def add_to_wishlist():
    """Add item to wishlist"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data.get('product_id'):
            return jsonify({'error': 'Product ID is required'}), 400
        
        # Check if product exists
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(
            user_id=user.id,
            product_id=data['product_id']
        ).first()
        
        if existing:
            return jsonify({'error': 'Product already in wishlist'}), 400
        
        # Add to wishlist
        wishlist_item = Wishlist(
            user_id=user.id,
            product_id=data['product_id']
        )
        
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to wishlist',
            'wishlist_item': wishlist_item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add to wishlist', 'message': str(e)}), 500

@bp.route('/<int:wishlist_id>', methods=['DELETE'])
@jwt_required_custom
def remove_from_wishlist(wishlist_id):
    """Remove item from wishlist"""
    try:
        user = get_current_user()
        wishlist_item = Wishlist.query.filter_by(id=wishlist_id, user_id=user.id).first()
        
        if not wishlist_item:
            return jsonify({'error': 'Wishlist item not found'}), 404
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from wishlist'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove from wishlist', 'message': str(e)}), 500
