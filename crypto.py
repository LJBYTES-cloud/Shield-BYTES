from cryptography.fernet import Fernet, InvalidToken
import base64

def _key_to_fernet(key: bytes) -> Fernet:
    base64_key = base64.urlsafe_b64encode(key[:32])
    return Fernet(base64_key)

def encrypt_data(data: bytes, key: bytes) -> bytes:
    f = _key_to_fernet(key)
    return f.encrypt(data)

def decrypt_data(token: bytes, key: bytes) -> bytes:
    f = _key_to_fernet(key)
    try:
        return f.decrypt(token)
    except InvalidToken:
        return None
