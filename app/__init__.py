# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from .config import get_config
import os

db = SQLAlchemy()
mail = Mail()
DB_NAME = "database.db"

def create_app(mode='default'):
    app = Flask(__name__)

    # Load configuration from config file
    app.config.from_object(get_config(mode))

    # Configure the upload folder
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize database
    db.init_app(app)

    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    # Initialize Flask-Mail
    mail.init_app(app)

    # Register blueprints
    from .auth import auth
    from .view import view

    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models and create tables
    from .models import User, Text, File
    with app.app_context():
        db.create_all()

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
