"""
Main entry point for the Flask application
"""
import sys
from app import create_app, db
from app.models.user import User
from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from app.models.review import Review
from werkzeug.security import generate_password_hash

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database with tables and default data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@ecommerce.com').first()
        if not admin:
            # Create default admin user
            admin = User(
                email='admin@ecommerce.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            db.session.add(admin)
            print("✓ Default admin user created")
            print("  Email: admin@ecommerce.com")
            print("  Password: admin123")
        
        # Create default categories
        if Category.query.count() == 0:
            categories = [
                Category(name='Electronics', description='Electronic devices and gadgets'),
                Category(name='Clothing', description='Fashion and apparel'),
                Category(name='Books', description='Books and publications'),
                Category(name='Home & Garden', description='Home and garden products'),
                Category(name='Sports', description='Sports and outdoor equipment'),
                Category(name='Toys', description='Toys and games'),
            ]
            db.session.add_all(categories)
            print("✓ Default categories created")
        
        db.session.commit()
        print("\n✓ Database initialization complete!")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        with app.app_context():
            init_db()
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
