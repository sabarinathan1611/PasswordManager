# functions.py
from flask_mail import Message
from flask import url_for
from . import mail
from .Converter import Converter
import os
import  json
import uuid
import logging
from flask  import current_app as app
from cryptography.fernet import Fernet
import os
import threading
from .dataencryption import AESCipher 
from . import scheduler
from datetime import  datetime
import logging
from logging.handlers import RotatingFileHandler
from .DeleteTask import delete_user_files_and_data

#scheduler.add_job(id='minute_task', func=delete_user_files_and_data, trigger='interval', minutes=1)
scheduler.add_job(id='daily_task', func=delete_user_files_and_data, trigger='cron', hour=0, minute=0)

aes_cipher = AESCipher()
def send_verification_email(user):
    verification_link = url_for('auth.verify_email', verification_token=user.verification_token, _external=True)
    subject = 'Verify Your Email for Web App'
    body = f'Click the following link to verify your email: {verification_link}'
    email=aes_cipher.decrypt_data(user.email)
    print("Email")
    send_email(email, subject, body)

def send_email(to, subject, body):
    sender=os.environ.get('GMAIL_USERNAME')
    print("SENDER MAIL: ",sender)
    msg = Message(subject, sender=os.environ.get('GMAIL_USERNAME'), recipients=[to])
    msg.body = body
    mail.send(msg)

def dict_to_string(input_dict):
    """
    Convert a dictionary to a string.
    
    Args:
        input_dict (dict): The dictionary to be converted.
    
    Returns:
        str: The converted string.
    """
    return json.dumps(input_dict)

def string_to_dict(input_string):
    """
    Convert a string to a dictionary.
    
    Args:
        input_string (str): The string to be converted.
    
    Returns:
        dict: The converted dictionary.
    """
    return json.loads(input_string)

def generate_filename(types):
    if types == 'der':
        return  str(uuid.uuid4()) + '.der'
    elif types == 'file':

        return  str(uuid.uuid4())




def makedir():
    uuid_str = str(uuid.uuid4())
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    private_key_keypath = os.path.join(APP_ROOT, f'static/key/private_key/{uuid_str}')
    public_key_keypath = os.path.join(APP_ROOT, f'static/key/public_key/{uuid_str}')

    print('keypath', private_key_keypath, public_key_keypath)
    uploadfolder = os.path.join(APP_ROOT, f'static/uploads/{uuid_str}')
    try:
        if not (os.path.exists(private_key_keypath) and os.path.exists(public_key_keypath) and os.path.exists(uploadfolder)):
            os.makedirs(private_key_keypath, exist_ok=True)
            os.makedirs(public_key_keypath, exist_ok=True)
            os.makedirs(uploadfolder, exist_ok=True)
        else:
            print("Folder Already Exists")
    except OSError as e:
        print(e)
    return uuid_str+'/'




def get_folder_size(folder_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
        inGB=Converter.convert_to_GB(total_size)
    return inGB




