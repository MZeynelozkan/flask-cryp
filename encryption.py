# encryption.py

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def generate_key(password: str, salt: bytes) -> bytes:
    # Verilen parola ve tuz ile bir anahtar oluşturur
    # Generates a key using the given password and salt
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_file(file_path: str, key: bytes):
    # Verilen dosyayı belirtilen anahtar ile şifreler
    # Encrypts the given file with the specified key
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)
    with open(file_path, 'wb') as file:
        file.write(encrypted)

def decrypt_file(file_path: str, key: bytes):
    # Verilen dosyanın şifresini belirtilen anahtar ile çözer
    # Decrypts the given file with the specified key
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    with open(file_path, 'wb') as file:
        file.write(decrypted)
