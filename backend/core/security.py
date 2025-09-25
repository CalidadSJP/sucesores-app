import os
from cryptography.fernet import Fernet
from config import Config

def load_signature_key():
    with open(Config.SIGNATURE_KEY_PATH, 'rb') as key_file:
        return Fernet(key_file.read())

# Variable global para reutilizar
fernet = load_signature_key()
