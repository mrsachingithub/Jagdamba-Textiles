from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user
from app.models import Product, Category

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # Mocking stats for now, can replace with real DB queries
    stats = {
        'products': 500,
        'customers': 1000,
        'variants': 2000,
        'orders': 5000
    }
    # Get some featured products (e.g., first 4)
    products = Product.query.limit(4).all()
    return render_template('index.html', title='Home', stats=stats, products=products)

@bp.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
        
    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()
    
    return render_template('shop.html', title='Shop', products=products.items, categories=categories, next_url=products.next_num, prev_url=products.prev_num)

@bp.route('/product/<int:id>')
def product_details(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', title=product.name, product=product)

@bp.route('/my-orders')
@login_required
def my_orders():
    from app.models import Order
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('user_dashboard.html', title='My Orders', orders=orders)

@bp.route('/collections')
def collections():
    categories = Category.query.all()
    return render_template('collections.html', title='Collections', categories=categories)

@bp.route('/about')
def about():
    return render_template('about.html', title='About Us')
