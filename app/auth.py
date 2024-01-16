from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify

auth = Blueprint('auth', __name__)


@auth.route('/login',methods=['POST'])
def login():
    admin = Emp_login.query.filter_by(email='vsabarinathan1611@gmail.com').first()
    if admin:
        if request.method == 'POST':
            
            email = request.form.get('email')
            password = request.form.get('passsword')

            dbemail = Emp_login.query.filter_by(email=email).first()
            print(dbemail)
            if dbemail :
                if check_password_hash(dbemail.password, password):

                    login_user(dbemail, remember=True)
    return render_template('login.html')

@auth.route('/sign-up',methods=['POST'])
def sign_up():
    pass
