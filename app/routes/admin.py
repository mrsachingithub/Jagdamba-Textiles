from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, ProductVariant, Order, ContactMessage
from functools import wraps
import os

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin')
@login_required
@admin_required
def dashboard():
    products_count = Product.query.count()
    orders_count = Order.query.count()
    return render_template('admin/dashboard.html', products_count=products_count, orders_count=orders_count)

@bp.route('/admin/products')
@login_required
@admin_required
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=20)
    return render_template('admin/products.html', products=products)

@bp.route('/admin/product/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_product():
    categories = Category.query.all()
    if request.method == 'POST':
        # Simple Logic for now - validation should be improved
        name = request.form.get('name')
        base_price = float(request.form.get('base_price'))
        category_id = int(request.form.get('category_id'))
        
        product = Product(name=name, base_price=base_price, category_id=category_id, 
                          description=request.form.get('description'),
                          width=request.form.get('width'),
                          fabric_type=request.form.get('fabric_type'))
        db.session.add(product)
        db.session.commit()
        
        # Add Initial Variant (Required for image)
        color_name = request.form.get('color_name')
        image_url = request.form.get('image_url') # In real app, handle file upload
        if color_name and image_url:
            variant = ProductVariant(product_id=product.id, color_name=color_name, image_url=image_url)
            db.session.add(variant)
            db.session.commit()
            
        flash('Product created successfully.')
        return redirect(url_for('admin.products'))
        
    return render_template('admin/product_form.html', categories=categories, title="New Product")

@bp.route('/admin/orders')
@login_required
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders)

@bp.route('/admin/messages')
@login_required
@admin_required
def messages():
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/messages.html', messages=messages)

@bp.route('/admin/order/<int:id>')
@login_required
@admin_required
def order_details(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_details.html', order=order)
