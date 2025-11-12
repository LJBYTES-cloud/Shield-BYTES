# Shield-BYTES - Desktop Password Manager [INSTALL EDITION]

## Overview

**Shield-BYTES** is an offline Bitwarden-inspired desktop password manager written in Python.  
It allows you to securely store login credentials (site, username, password) in a local encrypted vault, protected by a master password.  
The app uses a simple GUI and stores all sensitive data only on your device.

---

## Features

- Local vault file encrypted using your master password
- Ability to add, edit, delete, and view credentials
- Simple, clean Tkinter desktop GUI (cross-platform)
- No cloud, browser sync, or autofill (for security and simplicity)

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/LJBYTES-cloud/Shield-BYTES.git
   cd Shield-BYTES
   ```

2. **Install dependencies**
   - Make sure you have Python 3.10 or newer.
   - Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Usage**
   - On first run, set a master password (minimum 6 characters).
   - Log in with your master password on future runs.
   - Use the GUI to add, edit, or delete credentials.
   - Remember to save your vault before exiting!

---

## File Overview

- `main.py` — Application entry point, launches the Tkinter GUI.
- `ui.py` — User interface logic and all screens/windows.
- `auth.py` — Master password, authentication, and key derivation.
- `crypto.py` — Data encryption/decryption helpers.
- `vault.py` — CRUD operations for credential storage.
- `models.py` — Simple data class for credentials (site, username, password).
- `requirements.txt` — Python dependencies (cryptography).
- `config.json` — Stores (securely) your hashed master password and vault encryption salt (auto-generated).
- `vault.dat` — Your encrypted vault data (auto-generated).

---

## Security Notice

- Your master password is never stored directly, only a secure hash and random salt.
- All vault data is encrypted with a key derived from your master password.
- This project is for educational use and not intended for high-security production.

---

## Problems or Feature Requests?

Open an issue or pull request on [GitHub](https://github.com/LJBYTES-cloud/Shield-BYTES).

---
