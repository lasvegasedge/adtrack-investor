from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adtrack_investor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'noreply@adtrack.online'
    app.config['MAIL_PASSWORD'] = 'password'
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@adtrack.online'
    
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
    
    # Create database tables
    with app.app_context():
        from src.models.user import User
        db.create_all()
    
    return app
