# AVault 🔐

A simple and secure desktop password manager built with Python and Tkinter.

---

## Features

- 🔑 Master password protection with encryption
- 🗄️ Store and manage email/password pairs
- 🔒 All data encrypted using **Fernet (AES-128)** symmetric encryption
- 🗃️ Local SQLite database storage
- ⚠️ Auto-reset vault after 3 failed login attempts
- 🖥️ Simple and clean GUI using Tkinter

---

## Requirements

- Python 3.x
- `cryptography` library
- `tkinter` (usually pre-installed with Python)
- `sqlite3` (built-in with Python)

Install dependencies:

```bash
pip install cryptography
```

---

## How to Run

```bash
python AVault.py
```

---

## How It Works

1. On first launch, enter a master password — it gets encrypted and saved locally.
2. On next launches, enter your master password to unlock the vault.
3. After **3 wrong attempts**, the vault resets and all data is deleted.
4. Inside the vault you can:
   - **Insert** — add a new email and password
   - **Show** — view all saved credentials (decrypted)
   - **Remove** — delete a selected entry

---

## File Structure

```
~/.sstm/
├── keyp.key       # Encryption key for the database
├── key.key        # Encryption key for the master password
├── passwd.txt     # Encrypted master password
└── mydatabase.db  # SQLite database with encrypted credentials
```

---

## Security Notes

- All passwords are encrypted before being stored in the database.
- Encryption keys are stored locally in `~/.sstm/`.
- **Do not share or delete** the key files — you will lose access to your data.

---

## Author

**assanabopy-stack**  
[github.com/assanabopy-stack](https://github.com/assanabopy-stack)
