from app import create_app, db
from app.models import User, Category, Product, ProductVariant, Order, OrderItem

app = create_app()

def init_db():
    with app.app_context():
        # db.drop_all() # Uncomment to reset db
        db.create_all()
        print("Database tables created successfully.")
        
        # Create a test admin user if not exists
        if not User.query.filter_by(username='admin').first():
            import os
            password = os.environ.get('ADMIN_PASSWORD') or 'admin123'
            admin = User(username='admin', email='admin@jagdambatextiles.com', is_admin=True)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin/admin123")

if __name__ == '__main__':
    init_db()
