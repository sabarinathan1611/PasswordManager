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
    path=db.Column(db.String(100), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(32), default=secrets.token_urlsafe)
    used_storage=db.Column(db.Integer,default=0)
    limited_storage=db.Column(db.Integer,nullable=False,default=209715200)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    private_key_path= db.Column(db.String(200), nullable=False)
    public_key_path= db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mimetype=db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class DeleteAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  
    email = db.Column(db.String(100),  nullable=False)
    deleted=db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    email= db.Column(db.String,nullable=False)
    text = db.Column(db.String,nullable=False)