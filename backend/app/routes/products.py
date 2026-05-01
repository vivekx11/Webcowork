"""
Product routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product, Category
from app.middleware.auth import admin_required
from app.utils.validators import validate_required_fields, validate_positive_number, validate_integer
from app.utils.imagekit_helper import imagekit_helper
import base64

bp = Blueprint('products', __name__, url_prefix='/api/products')

@bp.route('', methods=['GET'])
def get_products():
    """Get all products with pagination and filters"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc')
        
        # Build query
        query = Product.query.filter_by(is_active=True)
        
        # Apply filters
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # Apply sorting
        if sort_by == 'price':
            query = query.order_by(Product.price.desc() if order == 'desc' else Product.price.asc())
        elif sort_by == 'name':
            query = query.order_by(Product.name.desc() if order == 'desc' else Product.name.asc())
        else:
            query = query.order_by(Product.created_at.desc() if order == 'desc' else Product.created_at.asc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'products': [product.to_dict() for product in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch products', 'message': str(e)}), 500

@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict(include_reviews=True)}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch product', 'message': str(e)}), 500

@bp.route('', methods=['POST'])
@admin_required
def create_product():
    """Create a new product (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'price', 'category_id', 'stock']
        is_valid, error = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Validate price
        is_valid, error = validate_positive_number(data['price'], 'Price')
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Validate stock
        is_valid, error = validate_integer(data['stock'], 'Stock')
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Check if category exists
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Handle image upload
        image_url = None
        image_id = None
        if 'image' in data and data['image']:
            # Assuming base64 encoded image
            upload_result = imagekit_helper.upload_image(
                file=data['image'],
                file_name=data['name'].replace(' ', '_'),
                folder='products'
            )
            
            if upload_result['success']:
                image_url = upload_result['url']
                image_id = upload_result['file_id']
        
        # Create product
        product = Product(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            category_id=data['category_id'],
            stock=int(data['stock']),
            image_url=image_url,
            image_id=image_id,
            sku=data.get('sku')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create product', 'message': str(e)}), 500

@bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update a product (Admin only)"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            is_valid, error = validate_positive_number(data['price'], 'Price')
            if not is_valid:
                return jsonify({'error': error}), 400
            product.price = float(data['price'])
        if 'category_id' in data:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Category not found'}), 404
            product.category_id = data['category_id']
        if 'stock' in data:
            is_valid, error = validate_integer(data['stock'], 'Stock')
            if not is_valid:
                return jsonify({'error': error}), 400
            product.stock = int(data['stock'])
        if 'sku' in data:
            product.sku = data['sku']
        if 'is_active' in data:
            product.is_active = bool(data['is_active'])
        
        # Handle image update
        if 'image' in data and data['image']:
            # Delete old image if exists
            if product.image_id:
                imagekit_helper.delete_image(product.image_id)
            
            # Upload new image
            upload_result = imagekit_helper.upload_image(
                file=data['image'],
                file_name=product.name.replace(' ', '_'),
                folder='products'
            )
            
            if upload_result['success']:
                product.image_url = upload_result['url']
                product.image_id = upload_result['file_id']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update product', 'message': str(e)}), 500

@bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete a product (Admin only)"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Delete image from ImageKit
        if product.image_id:
            imagekit_helper.delete_image(product.image_id)
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete product', 'message': str(e)}), 500
