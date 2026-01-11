import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-prod'
    
    # Database Configuration
    # Fallback to SQLite if DATABASE_URL is not set, for local development ease
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
    
    # Business Info
    BUSINESS_NAME = "Jagdamba Textiles"
    BUSINESS_ADDRESS = "Jagdamba Textiles 5062, New Pashupati Market, Ring Road, Surat, India – 395004"
    BUSINESS_INSTAGRAM = "https://instagram.com/jagdamba_textile_5062"
    BUSINESS_FACEBOOK = "#" # Update when link provided
