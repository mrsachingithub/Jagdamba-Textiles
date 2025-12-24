from app import create_app
from app.models import Category, Product

app = create_app()
with app.app_context():
    crepe = Category.query.filter_by(name='Crepe').first()
    if crepe:
        products = Product.query.filter_by(category_id=crepe.id).all()
        print(f"Products in Crepe: {[p.name for p in products]}")
    else:
        print("Crepe category not found")
