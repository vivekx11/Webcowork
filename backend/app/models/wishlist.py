"""
Wishlist model
"""
from app import db
from datetime import datetime

class Wishlist(db.Model):
    """Wishlist model for user's favorite products"""
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate wishlist items
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_wishlist_item'),)
    
    def to_dict(self):
        """Convert wishlist object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Wishlist {self.id}>'
