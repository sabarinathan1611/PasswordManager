from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login',methods=['POST','GET'])
def login():

    if request.method == 'POST':
            
            email = request.form.get('email')
            password = request.form.get('password')

            dbemail = User.query.filter_by(email=email).first()
            print(dbemail)
            if dbemail :
                print("Password",dbemail.password)
                if check_password_hash(dbemail.password, password):

                    login_user(dbemail, remember=True)
                return redirect(url_for('view.home'))

    return render_template('login.html')

@auth.route('/sign-up',methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('fullname')
        password = generate_password_hash(password)
        user=User(email=email,password=password,username=name)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))


    return render_template('Signup.html')