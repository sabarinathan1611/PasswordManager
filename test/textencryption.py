import hashlib
from Crypto.Cipher import AES
import configparser

class CryptoBase:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file

    def read_password_from_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        password = config.get('Encryption', 'password')
        return password

    def pad_data(self, data):
        block_size = AES.block_size
        padding = block_size - (len(data) % block_size)
        if isinstance(data, str):
            data = data.encode()
        return data + bytes([padding] * padding)

    def unpad_data(self, data):
        padding = data[-1]
        return data[:-padding]

class Encryption(CryptoBase):
    def encrypt_text(self, plaintext):
        password = self.read_password_from_config()
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_data = cipher.encrypt(self.pad_data(plaintext))
        return encrypted_data

class Decryption(CryptoBase):
    def decrypt_text(self, ciphertext):
        password = self.read_password_from_config()
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = self.unpad_data(cipher.decrypt(ciphertext)).decode()
        return decrypted_data

# Example usage
encryption_instance = Encryption()
decryption_instance = Decryption()

# Encrypt text
encrypted_text = encryption_instance.encrypt_text('Hello, this is a secret message.')

# Decrypt text
decrypted_text = decryption_instance.decrypt_text(encrypted_text)

print("Original Text:", 'Hello, this is a secret message.')
print("Encrypted Text:", encrypted_text)
print("Decrypted Text:", decrypted_text)
