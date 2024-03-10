from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import secrets
class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    encrypted_Key=db.Column(db.String(200))
    ciphertext=db.Column(db.String(200))
    nonce=db.Column(db.String(200))
    private_key_path= db.Column(db.String(200), nullable=False)
    public_key_path= db.Column(db.String(200), nullable=False)
    store_type=db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    texts = db.relationship('Text', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    role =  db.Column(db.String(100),nullable=False,default='user')
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(32), default=secrets.token_urlsafe)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filetype = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    private_key_path= db.Column(db.String(200), nullable=False)
    public_key_path= db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
