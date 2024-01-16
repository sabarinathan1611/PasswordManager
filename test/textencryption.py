import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import configparser

class CryptoBase:
    def __init__(self, config_file='config.ini'):
        """
        Initialize the CryptoBase class.

        :param config_file: Path to the configuration file.
        """
        self.config_file = config_file

    def read_password_from_config(self):
        """
        Read the encryption password from the configuration file.

        :return: Password for encryption.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)
        password = config.get('Encryption', 'password')
        return password

    def derive_key(self, password, salt, iterations=100000, key_length=32):
        """
        Derive a key from the password using PBKDF2.

        :param password: Password to derive the key from.
        :param salt: Salt used in the key derivation.
        :param iterations: Number of iterations for PBKDF2.
        :param key_length: Length of the derived key.
        :return: Derived key.
        """
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, key_length)
        return key

    def pad_data(self, data):
        """
        Pad the data to match the block size of the encryption algorithm.

        :param data: Data to be padded.
        :return: Padded data.
        """
        block_size = AES.block_size
        padding = block_size - (len(data) % block_size)
        if isinstance(data, str):
            data = data.encode()
        return data + bytes([padding] * padding)

    def unpad_data(self, data):
        """
        Unpad the data after decryption.

        :param data: Padded data.
        :return: Unpadded data.
        """
        padding = data[-1]
        return data[:-padding]

class Encryption(CryptoBase):
    def encrypt_text(self, plaintext):
        """
        Encrypt the input text using AES in CBC mode.

        :param plaintext: Text to be encrypted.
        :return: Encrypted data.
        """
        password = self.read_password_from_config()
        salt = get_random_bytes(16)  # Generate a random salt for each encryption
        key = self.derive_key(password, salt)
        iv = get_random_bytes(AES.block_size)  # Generate a random IV for CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(self.pad_data(plaintext))
        return salt + iv + encrypted_data

class Decryption(CryptoBase):
    def decrypt_text(self, ciphertext):
        """
        Decrypt the input ciphertext using AES in CBC mode.

        :param ciphertext: Encrypted data.
        :return: Decrypted text.
        """
        password = self.read_password_from_config()
        salt = ciphertext[:16]  # Extract the salt from the ciphertext
        iv = ciphertext[16:32]  # Extract the IV from the ciphertext
        key = self.derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = self.unpad_data(cipher.decrypt(ciphertext[32:])).decode()
        return decrypted_data

# Example usage
input_text = input('Original Text:')
encryption_instance = Encryption()
decryption_instance = Decryption()

# Encrypt text
encrypted_text = encryption_instance.encrypt_text(input_text)

# Decrypt text
decrypted_text = decryption_instance.decrypt_text(encrypted_text)

# Display results
print("Original Text:", input_text)
print("Encrypted Text:", encrypted_text)
print("Decrypted Text:", decrypted_text)
