from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from . import db
from .models import User
from flask_login import login_required,current_user
view = Blueprint('view', __name__)


@view.route('/',methods=['POST','GET'])
def home():
    return render_template('index.html')

@view.route('/home',methods=['POST','GET'])
@login_required
def log():
    return current_user.email

    
@view.route('/admin',methods=['POST','GET'])
@login_required
def admin():
    render_template ('admin.html')