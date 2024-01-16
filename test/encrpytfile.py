import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import configparser

class CryptoBase:
    def __init__(self, config_file='config.ini', debug_mode=False):
        self.config_file = config_file
        self.debug_mode = debug_mode

    def read_password_from_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        if self.debug_mode:
            # Print the sections and options for debug
            print("Sections:", config.sections())
            print("Options in 'Encryption' section:", config.options('Encryption'))

        password = config.get('Encryption', 'password')
        return password

    def derive_key(self, password, salt, iterations=100000, key_length=32):
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, key_length)
        return key

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
        salt = get_random_bytes(16)  # Generate a random salt for key derivation
        key = self.derive_key(password, salt)
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(input_filename, 'rb') as file:
            data = file.read()
        encrypted_data = cipher.encrypt(self.pad_data(data))
        with open(output_filename, 'wb') as file:
            file.write(salt + iv + encrypted_data)

class Decryption(CryptoBase):
    def decrypt_file(self, input_filename, output_filename):
        password = self.read_password_from_config()
        with open(input_filename, 'rb') as file:
            data = file.read()
        salt = data[:16]  # Extract the salt from the file
        key = self.derive_key(password, salt)
        iv = data[16:32]  # Extract the IV from the file
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = self.unpad_data(cipher.decrypt(data[32:]))
        with open(output_filename, 'wb') as file:
            file.write(decrypted_data)

# Example usage with debug mode off
encryption_instance = Encryption(debug_mode=True)
decryption_instance = Decryption(debug_mode=True)

# Encrypt a file
encryption_instance.encrypt_file('Test.png', 'encrypted_file.bin')

# Decrypt the file
decryption_instance.decrypt_file('encrypted_file.bin', 'decrypted_file.png')
