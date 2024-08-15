import  json
import uuid
from  dataencryption import AESCipher 
from TextEncryption import *
# from functions import string_to_hex
import sqlite3
import os
import random
import string
import secrets
aes_cipher=AESCipher()

def create_folder_if_not_exists(folder_path):
    """Creates a folder if it does not already exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

def string_to_hex(input_string):
    try:
        # Encode the string to bytes using UTF-8 encoding
        byte_value = input_string.encode('utf-8')
        
        # Convert each byte to its hexadecimal representation and join them
        hex_value = byte_value.hex()
        return hex_value.encode()
    except Exception as e:
        print(f"Error encoding string: {e}")
        return None
def generate_random_string(length=12):
    """Generates a random string of specified length."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_url():
    """Generates a random URL."""
    domains = ['.com', '.net', '.org', '.io', '.ai']
    protocol = 'https://'
    domain_name = generate_random_string(8)
    domain_extension = random.choice(domains)
    return f"{protocol}{domain_name}{domain_extension}"

def generate_random_name():
    """Generates a random name."""
    first_names = ['John', 'Jane', 'Alex', 'Emily', 'Chris', 'Katie', 'Michael', 'Laura']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_username():
    """Generates a random username."""
    return generate_random_string(8)

def generate_random_password(length=16):
    """Generates a random password."""
    return generate_random_string(length)

def generate_random_credentials():
    """Returns a tuple containing a random URL, name, username, and password."""
    url = generate_random_url()
    name = generate_random_name()
    username = generate_random_username()
    password = generate_random_password()
    return url, name, username, password


def store_pass(url,name,username,password,current_user_path,salt,id):



        keypath=os.path.join('/home/harish/Documents/cloud_management/app', 'static/key/')

        data={'url':url,'name':name,'username':username,'password':password,'keypath':keypath}

        
        string=json.dumps(data)
        create_folder_if_not_exists(os.path.join(keypath,'public_key',current_user_path))
        create_folder_if_not_exists(os.path.join(keypath,'private_key',current_user_path))


        public_key_path=os.path.join(keypath,'public_key',current_user_path,str(uuid.uuid4()) + '.der')

        print('public_key_path',public_key_path)

        encrypted_public=aes_cipher.encrypt_data(public_key_path)

        private_key_path=os.path.join(keypath,'private_key',current_user_path,str(uuid.uuid4()) + '.der')

        print('private_key_path',private_key_path)

        encrypted_private=aes_cipher.encrypt_data(private_key_path)

        encrypted_session_key, iv, ciphertext = text_encryption(public_key_path, private_key_path, string,salt=salt)

        stype=aes_cipher.encrypt_data("password")

        
        return id,encrypted_session_key, iv, ciphertext, encrypted_private, encrypted_public, stype



   
def add_pass():
    db_path = os.path.abspath('../instance/database.db')
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
    

    # Connect to the SQLite database
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA busy_timeout = 30000")  # Wait up to 30 seconds if the database is locked
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM user")
            ids=cursor.fetchall()
            user_ids = [user[0] for user in ids]
            for user_id in user_ids:
                cursor.execute("SELECT id,username, email, path FROM User WHERE id = ?", (user_id,))
                user = cursor.fetchone()
                if user:
                    data=[]
                    salt=aes_cipher.encrypt_data('admin')+string_to_hex('admin')
                    id,username, email, user_folder_path = user
                    print("\nName :",aes_cipher.decrypt_data(username))
                    print("Email :",aes_cipher.decrypt_data(email))
                    print("id :",id)
                    print("user_folder_path",user_folder_path,"\n")
                    for i in range(10):
                        url,name,username,password=generate_random_credentials()
                        datas=store_pass(url,name,username,password,user_folder_path,salt,id=id)
                        data.append(datas)

                    cursor.executemany(
    "INSERT INTO text (user_id, encrypted_Key, nonce, ciphertext, private_key_path, public_key_path, store_type) "
    "VALUES (?, ?, ?, ?, ?, ?, ?)", 
    data
)
                    conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            conn.close()
    except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            

add_pass()