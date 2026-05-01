"""
Order and OrderItem models
"""
from app import db
from datetime import datetime

class Order(db.Model):
    """Order model for customer orders"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, processing, shipped, delivered, cancelled
    payment_status = db.Column(db.String(20), default='pending', nullable=False)  # pending, paid, failed methods
    payment_method = db.Column(db.String(50))
    payment_id = db.Column(db.String(200))  # Stripe payment ID
    
    # Shipping information
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_state = db.Column(db.String(100), nullable=False)
    shipping_zip = db.Column(db.String(20), nullable=False)
    shipping_country = db.Column(db.String(100), nullable=False)
    shipping_phone = db.Column(db.String(20))
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_items=True):
        """Convert order object to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None,
            'user_email': self.user.email if self.user else None,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'payment_id': self.payment_id,
            'shipping_address': self.shipping_address,
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_zip': self.shipping_zip,
            'shipping_country': self.shipping_country,
            'shipping_phone': self.shipping_phone,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'item_count': len(self.order_items)
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.order_items]
        
        return data
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    """OrderItem model for items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at time of order
    
    def to_dict(self):
        """Convert order item object to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'product_image': self.product.image_url if self.product else None,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'
