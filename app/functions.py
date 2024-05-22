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
import sqlite3
from . import db
from sqlalchemy.orm import joinedload

def delete_user_files_and_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('../instance/database.db')
    cursor = conn.cursor()

    # Get the user IDs from DeleteAccount where deleted is False
    cursor.execute("SELECT user_id FROM DeleteAccount WHERE deleted = 0")
    users_to_delete = cursor.fetchall()
    
    # Extract user IDs from the query result
    user_ids = [user[0] for user in users_to_delete]
    
    for user_id in user_ids:
        # Load user data from User table
        cursor.execute("SELECT username, email FROM User WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            username, email = user
            print(f"User: {username}, Email: {email}")

            # Load and delete related files
            cursor.execute("SELECT id, filepath, private_key_path, public_key_path FROM File WHERE user_id = ?", (user_id,))
            files = cursor.fetchall()

            for file in files:
                try:
                    file_id, encrypted_filepath, encrypted_private_key_path, encrypted_public_key_path = file
                    filepath = aes_cipher.decrypt_data(encrypted_filepath)
                    private_key_path = aes_cipher.decrypt_data(encrypted_private_key_path)
                    public_key_path = aes_cipher.decrypt_data(encrypted_public_key_path)
                    print(f"Deleting file: {filepath}")

                    if os.path.exists(private_key_path):
                        os.remove(private_key_path)
                    else:
                        print(f"File not found: {private_key_path}")

                    if os.path.exists(public_key_path):
                        os.remove(public_key_path)
                    else:
                        print(f"File not found: {public_key_path}")

                    # Delete the file from the filesystem
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    else:
                        print(f"File not found: {filepath}")
                except Exception as e:
                    print(f"Error deleting file {filepath}: {e}")

            # Load and print related texts
            cursor.execute("SELECT id, private_key_path, public_key_path FROM Text WHERE user_id = ?", (user_id,))
            texts = cursor.fetchall()
            for text in texts:
                try:
                    text_id, encrypted_private_key_path, encrypted_public_key_path = text
                    private_key_path = aes_cipher.decrypt_data(encrypted_private_key_path)
                    public_key_path = aes_cipher.decrypt_data(encrypted_public_key_path)

                    if os.path.exists(private_key_path):
                        os.remove(private_key_path)
                    else:
                        print(f"File not found: {private_key_path}")

                    if os.path.exists(public_key_path):
                        os.remove(public_key_path)
                    else:
                        print(f"File not found: {public_key_path}")

                    print(f"Text ID: {text_id}, Encrypted Key: {text_id}")
                except Exception as e:
                    print(f"Error handling text {text_id}: {e}")

            # Optionally, delete the user and associated data from the database
            cursor.execute("DELETE FROM File WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM Text WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM User WHERE id = ?", (user_id,))
            conn.commit()

        else:
            print(f"User with ID {user_id} not found")

    # Update DeleteAccount table to set deleted to True
    cursor.execute("UPDATE DeleteAccount SET deleted = 1 WHERE user_id IN ({})".format(','.join('?' for _ in user_ids)), user_ids)
    conn.commit()

    print("Processing completed.")

    # Close the connection
    conn.close()



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




