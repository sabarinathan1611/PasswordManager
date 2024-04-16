# functions.py
from flask_mail import Message
from flask import url_for
from . import mail
import os
import  json
import uuid
import logging
from flask  import current_app as app
from cryptography.fernet import Fernet
import os
from .dataencryption import AESCipher 
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



