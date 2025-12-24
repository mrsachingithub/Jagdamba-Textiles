from app import create_app, db
from app.models import User, Product, Category, ProductVariant, Order # Import models to register with SQLA

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
