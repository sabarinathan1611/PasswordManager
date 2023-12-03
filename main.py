from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.argon2 import Argon2KDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

class TextEncryptor:
    def __init__(self, password):
        self.password = password

    def derive_key(self, salt, algorithm):
        if algorithm == "argon2":
            kdf = Argon2KDF(
                algorithm=hashes.Argon2id(),
                length=32,
                salt=salt,
                parallelism=2,
                memory_cost=65536,
                time_cost=2
            )
        elif algorithm == "pbkdf2":
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                iterations=100000,
                salt=salt,
                length=32
            )
        else:
            raise ValueError("Invalid algorithm")

        return kdf.derive(self.password.encode())

    def encrypt(self, text, algorithm="argon2"):
        salt = os.urandom(16)
        key = self.derive_key(salt, algorithm)

        cipher = Cipher(algorithms.AES(key), modes.CFB8(), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
        return urlsafe_b64encode(salt + ciphertext).decode()

    def decrypt(self, ciphertext, algorithm="argon2"):
        ciphertext = urlsafe_b64decode(ciphertext.encode())
        salt = ciphertext[:16]
        key = self.derive_key(salt, algorithm)

        cipher = Cipher(algorithms.AES(key), modes.CFB8(), backend=default_backend())
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
        return plaintext.decode()


class FileEncryptor:
    def __init__(self, password):
        self.password = password

    def derive_key(self, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=salt,
            length=32
        )
        return kdf.derive(self.password.encode())

    def encrypt(self, input_file, output_file):
        salt = os.urandom(16)
        key = self.derive_key(salt)

        with open(input_file, 'rb') as file:
            plaintext = file.read()

        cipher = Cipher(algorithms.AES(key), modes.CFB8(), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        with open(output_file, 'wb') as file:
            file.write(urlsafe_b64encode(salt + ciphertext))

    def decrypt(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            ciphertext = urlsafe_b64decode(file.read())

        salt = ciphertext[:16]
        key = self.derive_key(salt)

        cipher = Cipher(algorithms.AES(key), modes.CFB8(), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()

        with open(output_file, 'wb') as file:
            file.write(plaintext)


# Example usage for text
text_to_encrypt = "Hello, World!"
password_text = "secure_password"

text_encryptor = TextEncryptor(password_text)
encrypted_text = text_encryptor.encrypt(text_to_encrypt)
decrypted_text = text_encryptor.decrypt(encrypted_text)

print("Text Encrypted:", encrypted_text)
print("Text Decrypted:", decrypted_text)

# Example usage for file
input_file = "example.txt"
output_file = "encrypted_file.txt"
password_file = "secure_password"

file_encryptor = FileEncryptor(password_file)
file_encryptor.encrypt(input_file, output_file)

input_file = "encrypted_file.txt"
output_file = "decrypted_file.txt"
file_encryptor.decrypt(input_file, output_file)

