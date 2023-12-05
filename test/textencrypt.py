from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

class PasswordAESEncryptor:
    def __init__(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Use 16 for AES-128, 24 for AES-192, or 32 for AES-256
            salt=salt,
            iterations=100000,  # You may adjust the number of iterations based on your security requirements
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        self.cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

    def encrypt_text(self, plaintext):
        encryptor = self.cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode()

    def decrypt_text(self, ciphertext, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Use 16 for AES-128, 24 for AES-192, or 32 for AES-256
            salt=salt,
            iterations=100000,  # Same number of iterations as during encryption
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

        ciphertext = base64.b64decode(ciphertext)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()

if __name__ == "__main__":
    # Replace 'your_password' with the actual password
    password = '1234'
    salt = b'salt123'  # Use a unique salt for each user

    password_aes_encryptor = PasswordAESEncryptor(password, salt)

    # Text to encrypt
    plaintext = "Hello, this is a secret message!"

    # Encryption
    ciphertext = password_aes_encryptor.encrypt_text(plaintext)
    print(f"Encrypted Text: {ciphertext}")

    # Decryption
    entered_password = input("Enter the decryption password: ")
    
    # Validate the entered password
    if entered_password == password:
        decrypted_text = password_aes_encryptor.decrypt_text(ciphertext, entered_password)
        print(f"Decrypted Text: {decrypted_text}")
    else:
        print("Password is incorrect. Decryption failed.")
