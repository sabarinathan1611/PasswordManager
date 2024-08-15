import os
import base64
from Crypto.Cipher import AES
from dotenv import dotenv_values

class AESCipher:
    def __init__(self):
        self.env_vars = dotenv_values()
        key_encoded = self.env_vars.get("KEY")
        iv_encoded = self.env_vars.get("IV")
        self.key_bytes = bytes.fromhex(key_encoded)
        self.iv_bytes = bytes.fromhex(iv_encoded)

    def pad_data(self, data):
        # PKCS7 Padding
        pad_length = AES.block_size - (len(data) % AES.block_size)
        return data + bytes([pad_length] * pad_length)

    def unpad_data(self, padded_data):
        pad_length = padded_data[-1]
        return padded_data[:-pad_length]

    def encrypt_data(self, data):
        cipher = AES.new(self.key_bytes, AES.MODE_CBC, iv=self.iv_bytes)
        padded_data = self.pad_data(data.encode())
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext

    def decrypt_data(self, ciphertext):
        cipher = AES.new(self.key_bytes, AES.MODE_CBC, self.iv_bytes)
        decrypted_data = cipher.decrypt(ciphertext)
        return self.unpad_data(decrypted_data).decode()

# Example usage
aes_cipher = AESCipher()

# data = "12345678901234567890123ert6789012345678901234567890"
# encrypted_data = aes_cipher.encrypt_data(data)
# print("Encrypted data:", encrypted_data)
# print(len(encrypted_data))


# decrypted_data = aes_cipher.decrypt_data(encrypted_data)
# print("Decrypted data:", decrypted_data)



"""
Time: 
real    0m0.372s
user    0m0.258s
sys 0m0.110s

"""