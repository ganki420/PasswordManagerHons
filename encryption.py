from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

def get_key(): # function to make key
    key_file = "secret.key" # file
    if not os.path.exists(key_file): # if the key doesn't exist
        key = os.urandom(32)  # makes a AES-256 key
        with open(key_file, "wb") as f: # save key to file
            f.write(key)
    else:
        with open(key_file, "rb") as f: # loads existing key
            key = f.read()
    return key

def encrypt_password(password): # function to encrypt passwords
    key = get_key() # gets AES key
    cipher = AES.new(key, AES.MODE_CBC) # makes AES cipher in CBC mode
    ct_bytes = cipher.encrypt(pad(password.encode(), AES.block_size)) # pads and encrypts the password
    iv = base64.b64encode(cipher.iv).decode('utf-8') # encodes IV
    ct = base64.b64encode(ct_bytes).decode('utf-8') #encodes ciphertext
    return iv, ct  # Return both IV and encrypted password

def decrypt_password(iv, ct): # fucntion to decrypt passwords
    key = get_key() # gets the AES key
    iv = base64.b64decode(iv) # decodes IV from base64
    ct = base64.b64decode(ct) # decodes ciphertext from base64
    cipher = AES.new(key, AES.MODE_CBC, iv) # makes AES cipher with IV
    pt = unpad(cipher.decrypt(ct), AES.block_size) # decrypts and unpads
    return pt.decode('utf-8') # output password as text

def generate_key(): # make a key manually (only run it once)
    key = os.urandom(32)  # makes a AES-256 bit key
    with open("secret.key", "wb") as f: # save to file
        f.write(key)
    print(" Key generated successfully!")

# Uncomment the line below and run the script once to generate the key
#generate_key()