from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from .config import get_config
import os
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
from sqlalchemy import event
import logging

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
DB_NAME = "database.db"

def create_app(mode='default'):
    app = Flask(__name__)

    app.config.from_object(get_config(mode))

    # Configure the upload folder
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads/')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    KEY_FOLDER = os.path.join(app.root_path, 'static/key/')
    app.config['KEY_FOLDER'] = KEY_FOLDER

    # Initialize database
    db.init_app(app)

    # Initialize CSRF protection
    csrf.init_app(app)
    cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0", "supports_credentials": True}})

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
    create_database(app)

    return app

def create_database(app):
    if not os.path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

# def create_log(app):
#     log_formatter = logging.Formatter(
#         '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'
#     )

#     log_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
#     log_handler.setLevel(logging.INFO)
#     log_handler.setFormatter(log_formatter)
#     app.logger.addHandler(log_handler)

#     # Register SQLAlchemy event listeners for all models
#     with app.app_context():
#         @event.listens_for(db.engine, 'before_cursor_execute')
#         def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#             app.logger.info(f'Executing statement: {statement}')

#         @event.listens_for(db.engine, 'after_cursor_execute')
#         def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#             app.logger.info(f'Executed statement: {statement}')

#         for cls in db.Model._decl_class_registry.values():
#             if hasattr(cls, '__table__'):
#                 mapper = db.inspect(cls)
#                 @event.listens_for(mapper, 'after_insert')
#                 def after_insert_listener(mapper, connection, target):
#                     app.logger.info(f'Inserted record: {target}')

#                 @event.listens_for(mapper, 'after_update')
#                 def after_update_listener(mapper, connection, target):
#                     app.logger.info(f'Updated record: {target}')

#                 @event.listens_for(mapper, 'after_delete')
#                 def after_delete_listener(mapper, connection, target):
#                     app.logger.info(f'Deleted record: {target}')

