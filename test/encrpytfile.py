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
        return data + bytes([padding] * padding)

    def unpad_data(self, data):
        padding = data[-1]
        return data[:-padding]

class Encryption(CryptoBase):
    def encrypt_file(self, input_filename, output_filename):
        password = self.read_password_from_config()
        with open(input_filename, 'rb') as file:
            data = file.read()
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_data = cipher.encrypt(self.pad_data(data))
        with open(output_filename, 'wb') as file:
            file.write(encrypted_data)

class Decryption(CryptoBase):
    def decrypt_file(self, input_filename, output_filename):
        password = self.read_password_from_config()
        with open(input_filename, 'rb') as file:
            encrypted_data = file.read()
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = self.unpad_data(cipher.decrypt(encrypted_data))
        with open(output_filename, 'wb') as file:
            file.write(decrypted_data)

# Example usage
encryption_instance = Encryption()
decryption_instance = Decryption()

# Encrypt a file
encryption_instance.encrypt_file('Test.png', 'encrypted_file.bin')

# Decrypt the file
decryption_instance.decrypt_file('encrypted_file.bin', 'decrypted_file.png')
