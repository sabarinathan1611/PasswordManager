import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME')  # Use a custom environment variable for Gmail username
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')  # Use a custom environment variable for Gmail app-specific password
    AdminMail=os.environ.get('ADMINMAIL')


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(mode='default'):
    return config_by_name.get(mode, DevelopmentConfig)
