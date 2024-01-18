from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Text table
class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

class Password(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
     url=db.Column(db.String(150))
     username=db.Column(db.String(150))
     password = db.Column(db.String(100), nullable=False)



# User table
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    text = db.relationship('Text', backref=db.backref('users', lazy=True))
    date = db.Column(db.DateTime(timezone=True), default=func.now())



# Admin table
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    

# File table
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filetype = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('files', lazy=True))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

