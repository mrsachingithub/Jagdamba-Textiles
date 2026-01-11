from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from flask import current_app
import jwt
import time

class User(UserMixin, db.Model):
    __tablename__ = 'jagdamba_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Category(db.Model):
    __tablename__ = 'jagdamba_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False) # e.g., Georgette, Velvet
    image_url = db.Column(db.String(256)) # Optional representative image
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'jagdamba_product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, nullable=False)
    fabric_type = db.Column(db.String(64)) # Could be redundant if Category is fabric, but allows flexibility
    width = db.Column(db.String(32)) # e.g., "44 inches", "58 inches"
    category_id = db.Column(db.Integer, db.ForeignKey('jagdamba_category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    variants = db.relationship('ProductVariant', backref='product', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.name}>'

class ProductVariant(db.Model):
    __tablename__ = 'jagdamba_product_variant'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('jagdamba_product.id'), nullable=False)
    color_name = db.Column(db.String(64), nullable=False)
    hex_code = db.Column(db.String(16)) # Optional for UI color swatch
    image_url = db.Column(db.String(256), nullable=False)
    stock_quantity = db.Column(db.Integer, default=100)
    
    def __repr__(self):
        return f'<Variant {self.color_name} of {self.product_id}>'

class Order(db.Model):
    __tablename__ = 'jagdamba_order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('jagdamba_user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), default='Pending') # Pending, Paid, Shipped, Delivered, Cancelled
    razorpay_order_id = db.Column(db.String(100))
    razorpay_payment_id = db.Column(db.String(100))
    shipping_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'jagdamba_order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('jagdamba_order.id'), nullable=False)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('jagdamba_product_variant.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_at_purchase = db.Column(db.Float, nullable=False)

    # Helper to get product details quickly
    @property
    def product_name(self):
        variant = ProductVariant.query.get(self.product_variant_id)
        if variant:
            return f"{variant.product.name} ({variant.color_name})"
        return "Unknown Product"

class ContactMessage(db.Model):
    __tablename__ = 'jagdamba_contact_message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactMessage {self.email}>'
