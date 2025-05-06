import os
import tkinter as tk
from tkinter import messagebox
from backup.backup_utils import encrypt_data, decrypt_data

# file paths
KEY_FILE = "backup/backup.key"
BACKUP_FILE = "backup/backup.enc"
DB_FILE = "passwords.db"

def restore_database(): # function to restore from backup
    if not os.path.exists(KEY_FILE) or not os.path.exists(BACKUP_FILE):
        messagebox.showerror("Restore Failed", "Backup or key file not found.") #if didn't work
        return

    try:
        with open(KEY_FILE, "rb") as key_file: # read the encryption key
            key = key_file.read()

        with open(BACKUP_FILE, "rb") as enc_file: # read encrypted data
            encrypted_data = enc_file.read()

        decrypted_data = decrypt_data(encrypted_data, key) # decrypt backup

       # asks before overwriting the database
        result = messagebox.askyesno("Restore Backup", "This will overwrite your current database. Continue?")
        if not result:
            return

        with open(DB_FILE, "wb") as db_file: # overwriting database
            db_file.write(decrypted_data)

        messagebox.showinfo("Success", "Backup restored successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to restore backup.\n{str(e)}")

def backup_database(): # function to make encrypted databse backup
    if not os.path.exists(KEY_FILE):
        messagebox.showerror("Error", "Encryption key not found. Cannot create backup.")
        return

    try:
        with open(KEY_FILE, "rb") as key_file: # read encryption key
            key = key_file.read()

        with open(DB_FILE, "rb") as original_db: # read current database
            encrypted = encrypt_data(original_db.read(), key) # encrypt it

        with open(BACKUP_FILE, "wb") as backup_file: # save encrypted data
            backup_file.write(encrypted)

        messagebox.showinfo("Backup", "Encrypted backup saved as backup.enc.")
        
    except Exception as e:
        messagebox.show
