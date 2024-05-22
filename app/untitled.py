import sqlite3
from faker import Faker
import random
from datetime import datetime
import secrets
from .dataencryption import *
aes_cipher = AESCipher()


# Create an instance of Faker
fake = Faker()

# Connect to the SQLite database
conn = sqlite3.connect('../instance/database.db')
cursor = conn.cursor()

# Create the DeleteAccount table (if it doesn't already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS DeleteAccount (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    email TEXT NOT NULL,
    deleted BOOLEAN DEFAULT 0
)
''')

# Create the User table (if it doesn't already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    role TEXT DEFAULT 'user',
    path TEXT UNIQUE NOT NULL,
    is_verified BOOLEAN DEFAULT 0,
    verification_token TEXT DEFAULT '',
    used_storage INTEGER DEFAULT 0,
    limited_storage INTEGER DEFAULT 209715200
)
''')

# Function to insert random data into the tables
def insert_random_data(num_records):
    delete_account_data = []
    user_data = []

    for _ in range(num_records):
        # Generate data for User table
        username =  aes_cipher.encrypt_data(fake.user_name())
        email = aes_cipher.encrypt_data(fake.unique.email())
        password = aes_cipher.encrypt_data('1234')
        date = fake.date_time_this_decade()
        path = aes_cipher.encrypt_data(fake.unique.file_path())
        is_verified = fake.boolean()
        verification_token = aes_cipher.encrypt_data(secrets.token_urlsafe())
        used_storage = random.randint(0, 209715200)
        limited_storage = 209715200

        user_data.append((username, email, password, date, 'user', path, is_verified, verification_token, used_storage, limited_storage))

        # Generate data for DeleteAccount table
        user_id = _  # Assuming the user_id is a sequential integer starting from 0
        email = aes_cipher.encrypt_data(fake.unique.email())
        deleted = fake.boolean()

        delete_account_data.append((user_id, email, deleted))

    # Insert data into User table
    cursor.executemany('''
    INSERT INTO User (username, email, password, date, role, path, is_verified, verification_token, used_storage, limited_storage)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', user_data)

    # Insert data into DeleteAccount table
    cursor.executemany('''
    INSERT INTO DeleteAccount (user_id, email, deleted)
    VALUES (?, ?, ?)
    ''', delete_account_data)

    # Commit the transaction
    conn.commit()

# Insert 1,000,000 records into each table
insert_random_data(1000000)

# Close the connection
conn.close()
