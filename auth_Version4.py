import os
import json
import hashlib
from base64 import b64encode, b64decode

CONFIG_PATH = 'config.json'

def master_exists():
    return os.path.exists(CONFIG_PATH)

def set_master_password(password: str) -> None:
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    data = {
        'salt': b64encode(salt).decode(),
        'hash': b64encode(hashed).decode()
    }
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f)

def verify_master_password(password: str) -> bool:
    if not master_exists():
        return False
    with open(CONFIG_PATH, 'r') as f:
        data = json.load(f)
        salt = b64decode(data['salt'])
        stored_hash = b64decode(data['hash'])
    check_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return check_hash == stored_hash

def get_vault_key(password: str) -> bytes:
    with open(CONFIG_PATH, 'r') as f:
        data = json.load(f)
        salt = b64decode(data['salt'])
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return key