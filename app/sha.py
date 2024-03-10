import os
import base64
from Crypto.Cipher import AES
from dotenv import dotenv_values

# Load variables from .env file
env_vars = dotenv_values()

def pad_data(data):
    # PKCS7 Padding
    pad_length = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_length] * pad_length)

def unpad_data(padded_data):
    pad_length = padded_data[-1]
    return padded_data[:-pad_length]

def encrypt_data(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_data = pad_data(data.encode())
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext, cipher.iv

def decrypt_data(ciphertext, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    return unpad_data(decrypted_data).decode()

# Retrieve KEY and IV from environment variables
KEY_encoded = env_vars.get("KEY")
IV_encoded = env_vars.get("IV")

# Decode the keys from Base64 encoding
KEY_bytes = bytes(KEY_encoded.encode().decode('unicode-escape'), 'utf-8')
IV_bytes = bytes(IV_encoded.encode().decode('unicode-escape'), 'utf-8')
print("KEY_bytes:",KEY_bytes)
print("IV_bytes",IV_bytes)

# Example usage
data = "sabari"
encrypted_data, iv = encrypt_data(data, KEY_bytes, IV_bytes)
print("Encrypted data:", encrypted_data)
print("IV:", iv)

decrypted_data = decrypt_data(encrypted_data, iv, KEY_bytes)
print("Decrypted data:", decrypted_data) 
