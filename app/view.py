from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from . import db
from .models import User,Text
from flask_login import login_required,current_user
from .sysinfo import *
from .functions import dict_to_string,string_to_dict,generate_filename
from .forms import *
from flask  import current_app as app
from .TextEncryption import text_encryption,text_decryption
from .dataencryption import *
from .config import Config
import os
aes_cipher = AESCipher()
view = Blueprint('view', __name__)


@view.route('/',methods=['POST','GET'])
@login_required
def home():
    form = PasswordForm()
    if current_user.is_verified != True:
        
        return redirect(url_for('auth.logout'))

    return render_template('index.html',form=form)



    
@view.route('/admin',methods=['POST','GET'])
@login_required
def admin():
    
    if current_user.role == 'admin':
        system_info_printer = SystemInfoPrinter()
        storage_info= system_info_printer.print_storage_info()
        system_info =system_info_printer.print_system_info()

    else: 
        flash("You Don't have a Access")
        return redirect(url_for('view.home'))


    return render_template ('admin.html',storage_info=storage_info,system_info=system_info)

@view.route('/password',methods=['POST'])
def store_pass():
    form = PasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        url = form.url.data
        name=form.name.data
        username=form.username.data
        password=form.password.data
        keypath=app.config['KEY_FOLDER']
        data={'url':url,'name':name,'username':username,'password':password,'keypath':keypath}
        print("DATA: ",type(data))
        string=dict_to_string(data)
        public_key_path=keypath+generate_filename()
        print(public_key_path)
        encrypted_public=aes_cipher.encrypt_data(public_key_path)
        private_key_path=keypath+generate_filename()
        print(private_key_path)
        encrypted_private=aes_cipher.encrypt_data(private_key_path)

        encrypted_session_key, iv, ciphertext = text_encryption(public_key_path, private_key_path, string)
        stype=aes_cipher.encrypt_data("password")
        newtext =Text(user_id=current_user.id,encrypted_Key=encrypted_session_key,nonce=iv,ciphertext=ciphertext,private_key_path=encrypted_private,public_key_path=encrypted_public,store_type=stype)
        db.session.add(newtext)
        db.session.commit()
    return redirect(url_for('view.home'))

@view.route('/showpass',methods=['POST','GET'])
def showpass():
    if current_user.is_authenticated:
        passwords = Text.query.filter_by(user_id=current_user.id)
        data=[]
        for  password in passwords:
            decrypted_message=text_decryption(public_key_path=aes_cipher.decrypt_data(password.public_key_path),private_key_path=aes_cipher.decrypt_data(password.private_key_path),encrypted_session_key=password.encrypted_Key,iv=password.nonce,ciphertext=password.ciphertext)
            data.append({
                "id":password.id,
                "data":string_to_dict(decrypted_message),
                "store_type":aes_cipher.decrypt_data(password.store_type)
                })
        print("DATA:",data,'\n')
        
        return render_template('passwords.html', data=data)
    else:
        return redirect('/')

