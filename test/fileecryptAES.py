from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass
import os

class FileEncryptor:
    def __init__(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        self.key = key

    def encrypt_file(self, input_file, output_file):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(input_file, 'rb') as f_input, open(output_file, 'wb') as f_output:
            f_output.write(iv)

            chunk_size = 16 * 1024
            while chunk := f_input.read(chunk_size):
                encrypted_chunk = encryptor.update(chunk)
                f_output.write(encrypted_chunk)

class FileDecryptor:
    def __init__(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        self.key = key

    def decrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as f_input:
            iv = f_input.read(16)
            cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            with open(output_file, 'wb') as f_output:
                chunk_size = 16 * 1024
                while chunk := f_input.read(chunk_size):
                    decrypted_chunk = decryptor.update(chunk)
                    f_output.write(decrypted_chunk)

if __name__ == "__main__":
    password = getpass("Enter the encryption password: ")
    salt = os.urandom(16)

    encryptor = FileEncryptor(password, salt)
    decryptor = FileDecryptor(password, salt)

    input_file_path = './example.txt'
    encrypted_file_path = './encrypted_file.enc'
    decrypted_file_path = './decrypted_file.txt'

    # Encryption
    encryptor.encrypt_file(input_file_path, encrypted_file_path)
    print("File encryption complete.")

    # Decryption
    entered_password = getpass("Enter the decryption password: ")
    if entered_password == password:
        decryptor.decrypt_file(encrypted_file_path, decrypted_file_path)
        print("File decryption complete.")
    else:
        print("Password is incorrect. Decryption failed.")
