from app import create_app, db
from app.models import User, Product, Category, ProductVariant, Order
from seed_data import seed_database

app = create_app()

# Fail-safe: Create tables and seed data on every startup
# This ensures that even if Render skip build steps, the app works.
with app.app_context():
    db.create_all()
    seed_database()

if __name__ == '__main__':
    app.run(debug=True)
