from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Register Blueprints
    from app.routes import auth, main
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(main.bp)
    from app.routes import cart, admin
    app.register_blueprint(cart.bp)
    app.register_blueprint(admin.bp)

    # Temporary route to verify setup until blueprints are ready
    @app.route('/health')
    def health():
        return "Jagdamba Textiles App is Running!"

    # Context Processor for unread messages
    @app.context_processor
    def inject_unread_count():
        from flask_login import current_user
        if not current_user.is_authenticated or not current_user.is_admin:
            return dict(unread_messages_count=0)
        
        from app.models import ContactMessage
        count = ContactMessage.query.filter_by(is_read=False).count()
        return dict(unread_messages_count=count)

    return app
