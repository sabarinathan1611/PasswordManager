# functions.py
from flask_mail import Message
from flask import url_for
from . import mail
import os
def send_verification_email(user):
    verification_link = url_for('auth.verify_email', verification_token=user.verification_token, _external=True)
    subject = 'Verify Your Email for Web App'
    body = f'Click the following link to verify your email: {verification_link}'
    
    send_email(user.email, subject, body)

def send_email(to, subject, body):
    sender=os.environ.get('GMAIL_USERNAME')
    print("SENDER MAIL: ",sender)
    msg = Message(subject, sender=os.environ.get('GMAIL_USERNAME'), recipients=[to])
    msg.body = body
    mail.send(msg)
