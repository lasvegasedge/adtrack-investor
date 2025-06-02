from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
import os
import sys

# Add parent directory to path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adtrack_investor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with actual mail server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'noreply@adtrack.online'  # Replace with actual email
    app.config['MAIL_PASSWORD'] = 'password'  # Replace with actual password
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@adtrack.online'  # Replace with actual email
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    
    # Import and register blueprints
    from src.routes.auth import auth_bp
    from src.routes.main import main_bp
    from src.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Import models
    from src.models.user import User, PageView
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@adtrack.online').first()
        if not admin:
            admin = User(
                email='admin@adtrack.online',
                name='Admin User',
                role='admin',
                is_active=True,
                is_approved=True,
                email_confirmed=True,
                agreement_accepted=True
            )
            admin.set_password('adminpassword')  # Change this in production
            db.session.add(admin)
            db.session.commit()
    
    # Page view tracking middleware
    @app.before_request
    def track_page_view():
        if current_user.is_authenticated and request.endpoint != 'static':
            page_view = PageView(
                user_id=current_user.id,
                page_url=request.path
            )
            db.session.add(page_view)
            db.session.commit()
    
    return app
