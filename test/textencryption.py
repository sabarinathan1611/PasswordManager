from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import hmac
import hashlib
import base64

class CryptoAES:
    def __init__(self, key):
        self.key = key

    def encrypt_message(self, message):
        nonce = get_random_bytes(12)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        return ciphertext, cipher.nonce, tag

    def decrypt_message(self, nonce, ciphertext, tag):
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()

def derive_key(password, salt, key_length=32):
    key = PBKDF2(password, salt, dkLen=key_length)
    return key

def generate_random_nonce():
    return get_random_bytes(12)

def generate_mac(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()

def verify_mac(key, mac, data):
    expected_mac = generate_mac(key, data)
    return hmac.compare_digest(expected_mac, mac)

def generate_rsa_key_pair():
    key = RSA.generate(2048)
    return key.publickey(), key

def encrypt_symmetric_key(key, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(key)
    return encrypted_key

def decrypt_symmetric_key(encrypted_key, private_key):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    key = cipher_rsa.decrypt(encrypted_key)
    return key

class CryptoRSA:
    def __init__(self, public_key_path, private_key_path):
        with open(public_key_path, 'rb') as f:
            self.public_key = RSA.import_key(f.read())
        with open(private_key_path, 'rb') as f:
            self.private_key = RSA.import_key(f.read())

    def encrypt_message(self, message):
        session_key = get_random_bytes(16)
        encrypted_key = encrypt_symmetric_key(session_key, self.public_key)

        aes_cipher = CryptoAES(session_key)
        ciphertext, nonce, tag = aes_cipher.encrypt_message(message)

        return encrypted_key, base64.b64encode(nonce), base64.b64encode(tag), base64.b64encode(ciphertext)

    def decrypt_message(self, encrypted_key, nonce_b64, tag_b64, ciphertext_b64):
        print("Encrypted Key Length:", len(encrypted_key))  # Debugging
        encrypted_key = base64.b64decode(encrypted_key)
        print("Decoded Encrypted Key Length:", len(encrypted_key))  # Debugging

        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)
        ciphertext = base64.b64decode(ciphertext_b64)

        session_key = decrypt_symmetric_key(encrypted_key, self.private_key)

        aes_cipher = CryptoAES(session_key)
        decrypted_message = aes_cipher.decrypt_message(nonce, ciphertext, tag)
        return decrypted_message

def generate_key_pair(public_key_path, private_key_path):
    public_key, private_key = generate_rsa_key_pair()
    with open(public_key_path, 'wb') as f:
        f.write(public_key.export_key())
    with open(private_key_path, 'wb') as f:
        f.write(private_key.export_key())

def main():
    public_key_path = 'public_key.pem'
    private_key_path = 'private_key.pem'

    generate_key_pair(public_key_path, private_key_path)
    print("Public and private key pair generated successfully.")

    rsa_instance = CryptoRSA(public_key_path, private_key_path)

    message = "Tst"

    # Encrypt the message
    encrypted_key, nonce, tag, ciphertext = rsa_instance.encrypt_message(message)
    print("Encrypted Key:", base64.b64encode(encrypted_key))
    print("Nonce:", nonce)
    print("Tag:", tag)
    print("Ciphertext:", ciphertext)

    # Decrypt the message
    decrypted_message = rsa_instance.decrypt_message(encrypted_key, nonce, tag, ciphertext)
    print("Decrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()
