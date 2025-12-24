from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Product, ProductVariant, Order, OrderItem
import razorpay

bp = Blueprint('cart', __name__)

@bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total_amount = 0
    
    for variant_id, quantity in cart.items():
        variant = ProductVariant.query.get(int(variant_id))
        if variant:
            subtotal = variant.product.base_price * int(quantity)
            total_amount += subtotal
            cart_items.append({
                'variant': variant,
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    variant_id = request.form.get('variant_id')
    quantity = int(request.form.get('quantity', 1))
    
    cart = session.get('cart', {})
    
    if variant_id in cart:
        cart[variant_id] += quantity
    else:
        cart[variant_id] = quantity
        
    session['cart'] = cart
    flash('Item added to cart.')
    return redirect(url_for('cart.view_cart'))

@bp.route('/update_cart', methods=['POST'])
def update_cart():
    variant_id = request.form.get('variant_id')
    quantity = int(request.form.get('quantity'))
    
    cart = session.get('cart', {})
    
    if quantity > 0:
        cart[variant_id] = quantity
    else:
        cart.pop(variant_id, None)
        
    session['cart'] = cart
    return redirect(url_for('cart.view_cart'))

@bp.route('/remove_from_cart/<int:variant_id>')
def remove_from_cart(variant_id):
    cart = session.get('cart', {})
    variant_id = str(variant_id)
    if variant_id in cart:
        cart.pop(variant_id)
        session['cart'] = cart
        flash('Item removed from cart.')
    return redirect(url_for('cart.view_cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('main.shop'))
        
    total_amount = 0
    for variant_id, quantity in cart.items():
        variant = ProductVariant.query.get(int(variant_id))
        if variant:
            total_amount += variant.product.base_price * int(quantity)
            
    if request.method == 'POST':
        # Create Razorpay Order
        client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))
        payment_amount = int(total_amount * 100) # In paise
        data = { "amount": payment_amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        
        # Create Local Order (Pending)
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            status='Pending',
            razorpay_order_id=payment['id'],
            shipping_address=request.form.get('address')
        )
        db.session.add(order)
        
        for variant_id, quantity in cart.items():
            variant = ProductVariant.query.get(int(variant_id))
            if variant:
                item = OrderItem(
                    order=order,
                    product_variant_id=variant.id,
                    quantity=quantity,
                    price_at_purchase=variant.product.base_price
                )
                db.session.add(item)
        
        db.session.commit()
        
        return render_template('checkout.html', payment=payment, order=order, key_id=current_app.config['RAZORPAY_KEY_ID'])
        
    return render_template('checkout_form.html', total_amount=total_amount)

@bp.route('/payment_success', methods=['POST'])
@login_required
def payment_success():
    # Verify payment signature here in production
    # For now, assume success and clear cart
    session.pop('cart', None)
    flash('Order placed successfully!')
    return redirect(url_for('main.index')) # Redirect to order history later
