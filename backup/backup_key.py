# backup/backup_key.py
from cryptography.fernet import Fernet

key = Fernet.generate_key() # generates a secure random key

with open("backup/backup.key", "wb") as f: # save key to a file
    f.write(key)

print("Key saved to backup/backup.key") # confirm success
