import os
import json
from models import Credential
from crypto import encrypt_data, decrypt_data

VAULT_PATH = 'vault.dat'

def save_vault(credentials: list, key: bytes):
    data = [c.__dict__ for c in credentials]
    json_data = json.dumps(data).encode()
    encrypted = encrypt_data(json_data, key)
    with open(VAULT_PATH, 'wb') as f:
        f.write(encrypted)

def load_vault(key: bytes) -> list:
    if not os.path.exists(VAULT_PATH):
        return []
    with open(VAULT_PATH, 'rb') as f:
        encrypted = f.read()
    decrypted = decrypt_data(encrypted, key)
    if decrypted is None:
        raise ValueError("Failed to decrypt vault data.")
    data = json.loads(decrypted.decode())
    return [Credential(**c) for c in data]

def add_credential(credentials: list, cred: Credential):
    credentials.append(cred)

def edit_credential(credentials: list, index: int, cred: Credential):
    if 0 <= index < len(credentials):
        credentials[index] = cred

def delete_credential(credentials: list, index: int):
    if 0 <= index < len(credentials):
        del credentials[index]
