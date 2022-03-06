import random
import string
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from rsa import encrypt
from src.configuration.Settings import Settings
import base64

class PasswordService:

    _settings_ = Settings()
    key = _settings_.ENCRYPTION_KEY

    def generate_password(self):
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(20))
        return self.encrypt_password(password)
    
    #TODO: probar con assosiated data
    def encrypt_password(self, password):
        password = password.encode()
        nonce = secrets.token_bytes(12)
        password = nonce + AESGCM(self.key).encrypt(nonce, password, b'')
        return base64.b64encode(password).decode()

    def decrypt_password(self, password):
        password = base64.b64decode(password)
        password = AESGCM(self.key).decrypt(password[:12], password[12:], b'')
        return password.decode()
        
