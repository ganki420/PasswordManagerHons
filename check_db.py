import sqlite3

# Connect to database
conn = sqlite3.connect("passwords.db") # opens connection to the database
cursor = conn.cursor() # creates a cursor to run SQL

# Get stored passwords
cursor.execute("SELECT * FROM passwords") # get all passwords
rows = cursor.fetchall() # gets all rows
conn.close() # closes connection

# Print results
if rows:
    for row in rows:
        print(row)  # Prints each stored password
else:
    print("No passwords found in database.") # shows message if its empty