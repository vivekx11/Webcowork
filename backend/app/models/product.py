"""
Product and Category models
"""
from app import db
from datetime import datetime

class Category(db.Model):
    """Category model for product categorization"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        """Convert category object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_count': len(self.products)
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    """Product model for e-commerce items"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(500))
    image_id = db.Column(db.String(200))  # ImageKit file ID for deletion
    is_active = db.Column(db.Boolean, default=True)
    sku = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    cart_items = db.relationship('Cart', backref='product', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_reviews=False):
        """Convert product object to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'stock': self.stock,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'sku': self.sku,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'average_rating': self.get_average_rating(),
            'review_count': len(self.reviews)
        }
        
        if include_reviews:
            data['reviews'] = [review.to_dict() for review in self.reviews]
        
        return data
    
    def get_average_rating(self):
        """Calculate average rating for the product"""
        if not self.reviews:
            return 0
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)
    
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
    
    def __repr__(self):
        return f'<Product {self.name}>'
