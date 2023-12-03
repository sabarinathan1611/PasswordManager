

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.argon2 import Argon2KDF

def pbkdf2_hmac(password, salt, iterations=100000, length=32):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=iterations,
        salt=salt,
        length=length
    )
    key = kdf.derive(password.encode())
    return key

def argon2_kdf(password, salt, parallelism=2, memory_cost=65536, time_cost=2, length=32):
    kdf = Argon2KDF(
        algorithm=hashes.Argon2id(),
        length=length,
        salt=salt,
        parallelism=parallelism,
        memory_cost=memory_cost,
        time_cost=time_cost
    )
    key = kdf.derive(password.encode())
    return key
