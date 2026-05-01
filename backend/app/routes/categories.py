"""
Category routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Category
from app.middleware.auth import admin_required

bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@bp.route('', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.all()
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch categories', 'message': str(e)}), 500

@bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get single category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'category': category.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch category', 'message': str(e)}), 500

@bp.route('', methods=['POST'])
@admin_required
def create_category():
    """Create a new category (Admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Category name is required'}), 400
        
        # Check if category already exists
        if Category.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Category already exists'}), 400
        
        category = Category(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create category', 'message': str(e)}), 500

@bp.route('/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """Update a category (Admin only)"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update category', 'message': str(e)}), 500

@bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    """Delete a category (Admin only)"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check if category has products
        if category.products:
            return jsonify({'error': 'Cannot delete category with products'}), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete category', 'message': str(e)}), 500
