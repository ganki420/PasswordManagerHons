from cryptography.fernet import Fernet

def generate_key(): # function to make a new encryption key
    return Fernet.generate_key() # returns a random 32-byte key

# function to encrypt data using a key
def encrypt_data(data: bytes, key: bytes) -> bytes:
    f = Fernet(key) # makes a Fernet cipher
    return f.encrypt(data) # return encryptd data

# function to decrypt data using a key
def decrypt_data(data: bytes, key: bytes) -> bytes:
    f = Fernet(key) 
    return f.decrypt(data) # return decrypted data
