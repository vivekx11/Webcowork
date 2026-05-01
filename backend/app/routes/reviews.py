"""
Review routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.review import Review
from app.models.product import Product
from app.middleware.auth import jwt_required_custom, get_current_user
from app.utils.validators import validate_rating

bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    """Get all reviews for a product"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews],
            'average_rating': product.get_average_rating(),
            'review_count': len(reviews)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch reviews', 'message': str(e)}), 500

@bp.route('/product/<int:product_id>', methods=['POST'])
@jwt_required_custom
def create_review(product_id):
    """Create a review for a product"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Validate rating
        if not data.get('rating'):
            return jsonify({'error': 'Rating is required'}), 400
        
        is_valid, error = validate_rating(data['rating'])
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Check if user already reviewed this product
        existing_review = Review.query.filter_by(
            user_id=user.id,
            product_id=product_id
        ).first()
        
        if existing_review:
            return jsonify({'error': 'You have already reviewed this product'}), 400
        
        # Create review
        review = Review(
            user_id=user.id,
            product_id=product_id,
            rating=int(data['rating']),
            comment=data.get('comment', '')
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create review', 'message': str(e)}), 500

@bp.route('/<int:review_id>', methods=['PUT'])
@jwt_required_custom
def update_review(review_id):
    """Update a review"""
    try:
        user = get_current_user()
        review = Review.query.filter_by(id=review_id, user_id=user.id).first()
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        data = request.get_json()
        
        if 'rating' in data:
            is_valid, error = validate_rating(data['rating'])
            if not is_valid:
                return jsonify({'error': error}), 400
            review.rating = int(data['rating'])
        
        if 'comment' in data:
            review.comment = data['comment']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review updated successfully',
            'review': review.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update review', 'message': str(e)}), 500

@bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required_custom
def delete_review(review_id):
    """Delete a review"""
    try:
        user = get_current_user()
        review = Review.query.filter_by(id=review_id, user_id=user.id).first()
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': 'Review deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete review', 'message': str(e)}), 500
