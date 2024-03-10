from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

class CryptoRSA:
    def __init__(self, public_key_path, private_key_path):
        with open(public_key_path, 'rb') as f:
            self.public_key = RSA.import_key(f.read())
        with open(private_key_path, 'rb') as f:
            self.private_key = RSA.import_key(f.read())

    def encrypt_message(self, message):
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_CBC)
        ciphertext = cipher_aes.encrypt(self.pad_data(message.encode()))

        # Return the encrypted session key and ciphertext
        return base64.b64encode(encrypted_session_key), base64.b64encode(cipher_aes.iv), base64.b64encode(ciphertext)

    def decrypt_message(self, encrypted_session_key_b64, iv_b64, ciphertext_b64):
        encrypted_session_key = base64.b64decode(encrypted_session_key_b64)
        iv = base64.b64decode(iv_b64)
        ciphertext = base64.b64decode(ciphertext_b64)

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        session_key = cipher_rsa.decrypt(encrypted_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted_message = self.unpad_data(cipher_aes.decrypt(ciphertext))

        return decrypted_message.decode()

    def pad_data(self, data):
        block_size = AES.block_size
        padding = block_size - (len(data) % block_size)
        return data + bytes([padding] * padding)

    def unpad_data(self, data):
        padding = data[-1]
        return data[:-padding]

def generate_key_pair(public_key_path, private_key_path):
    key = RSA.generate(2048)
    with open(public_key_path, 'wb') as f:
        f.write(key.publickey().export_key())
    with open(private_key_path, 'wb') as f:
        f.write(key.export_key())

def main():
    public_key_path = 'public_key.pem'
    private_key_path = 'private_key.pem'

    generate_key_pair(public_key_path, private_key_path)
    print("Public and private key pair generated successfully.")

    rsa_instance = CryptoRSA(public_key_path, private_key_path)

    message = input("Enter the message to encrypt: ")

    # Encrypt the message
    encrypted_session_key, iv, ciphertext = rsa_instance.encrypt_message(message)
    print("Encrypted Key:", encrypted_session_key)
    print("Nonce:", iv)
    print("Tag:", ciphertext)

    # Decrypt the message
    decrypted_message = rsa_instance.decrypt_message(encrypted_session_key, iv, ciphertext)
    print("Decrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()
