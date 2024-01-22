from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .form import * 
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')  # Add a flash message
            return redirect(url_for('view.home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')  # Add a flash message

    return render_template('login.html', form=form)


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    form = SignUpForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.fullname.data
        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password, username=name)
        db.session.add(user)
        db.session.commit()

        # Log in the user after registration 
        login_user(user, remember=True)

        return redirect(url_for('view.home'))

    return render_template('Signup.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))