from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Product, Category, ContactMessage
from app import db

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

from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # In a real application, you would send an email here using Flask-Mail or an external API.
        # For now, we will just simulate a successful submission.
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Save to database
        msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(msg)
        db.session.commit()
        
        # Log the message (optional, for debugging)
        print(f"Contact Form Submission\nName: {name}\nEmail: {email}\nMessage: {message}")
        
        flash('Thank you for your message! We will get back to you shortly at jagdambatextiles5062@gmail.com.', 'success')
        return redirect(url_for('main.contact'))
        
    return render_template('contact.html', title='Contact Us')

@bp.route('/order/<int:id>')
@login_required
def order_details(id):
    from app.models import Order
    order = Order.query.get_or_404(id)
    # Ensure user owns the order
    if order.user_id != current_user.id:
        flash("You do not have permission to view this order.", "danger")
        return redirect(url_for('main.my_orders'))
        
    return render_template('order_details.html', title=f'Order #{order.id}', order=order)
