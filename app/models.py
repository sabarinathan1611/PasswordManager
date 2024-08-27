from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import secrets
from datetime import datetime
class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    encrypted_Key = db.Column(db.LargeBinary, nullable=False)  # should be bytes
    nonce = db.Column(db.LargeBinary, nullable=False)  # should be bytes
    ciphertext = db.Column(db.LargeBinary, nullable=False)  # should be bytes
    private_key_path = db.Column(db.LargeBinary, nullable=False)  # should be bytes
    public_key_path = db.Column(db.LargeBinary, nullable=False)  # should be bytes
    store_type = db.Column(db.LargeBinary, nullable=False)  # should be bytes
    date = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.LargeBinary, unique=True,nullable=True)
    email = db.Column(db.LargeBinary, unique=True,nullable=True)
    password = db.Column(db.String(), nullable=False)
    texts = db.relationship('Text', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    role =  db.Column(db.String(),nullable=False,default='user')
    path=db.Column(db.LargeBinary, unique=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(), default=secrets.token_urlsafe)
    used_storage=db.Column(db.Integer,default=0)
    limited_storage=db.Column(db.Integer,nullable=False,default=209715)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.LargeBinary, unique=True,nullable=True)
    filepath = db.Column(db.LargeBinary, unique=True,nullable=True)
    private_key_path= db.Column(db.LargeBinary, unique=True,nullable=True)
    public_key_path= db.Column(db.LargeBinary, unique=True,nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mimetype=db.Column(db.LargeBinary, unique=True,nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class DeleteAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  
    email = db.Column(db.LargeBinary, unique=True,nullable=False)
    deleted=db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.LargeBinary, unique=True,nullable=True)
    email= db.Column(db.LargeBinary, unique=True,nullable=True)
    text = db.Column(db.LargeBinary, unique=True,nullable=True)
    fixed=db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    