import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher() # making Argon2 hasher instance

def hash_password(password): # function to hash master password
    return ph.hash(password) # return the hashed version

def register_user(username, master_password): # funcction to register a new user
    hashed_password = hash_password(master_password) # hashes the password

    conn = sqlite3.connect('passwords.db', isolation_level=None) # connects to database
    cursor = conn.cursor()

    try: # insert username and hashed password into users table
        cursor.execute('''
            INSERT INTO users (username, master_password_hash)
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit() #saves the changes
        return True # the registration was successful
    except sqlite3.IntegrityError as e:
        print("IntegrityError:", e) # username already exists
        return False
    finally:
        cursor.close() # closes cursor
        conn.close() # closes connection

def authenticate_user(username, input_password):
    conn = sqlite3.connect("passwords.db") # connect to the database
    cursor = conn.cursor()

    # gets the user ID and hashed password from the database
    cursor.execute("SELECT id, master_password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone() # gets the first matching user
    conn.close() # close the database connecton

    if result:
        user_id, hashed_password = result
        try:
            if ph.verify(hashed_password, input_password):
                return user_id # login was successful
        except VerifyMismatchError:
            return None  # wrong password
    return None  # user not found or credentials are invaldi
