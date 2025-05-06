import sqlite3

def init_db():
    conn = sqlite3.connect('passwords.db') # connects to the database file
    conn.execute("PRAGMA journal_mode=WAL;")  # enable write-ahead logging mode
    cursor = conn.cursor() # makes a cursor to execute SQL commands

    # create users table (for authentication)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            master_password_hash TEXT NOT NULL
        )
    ''')

    # create passwords table (for storing encrypted credentials)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,  -- Link passwords to users
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password_iv TEXT NOT NULL,  -- IV for AES encryption
            encrypted_password TEXT NOT NULL,  -- Encrypted password
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit() # saves the changes
    conn.close() # closes connection

if __name__ == "__main__": 
    init_db()

