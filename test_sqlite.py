import sqlite3

try:
    conn = sqlite3.connect('contacts.db')
    print("Connection to contacts.db successful!")
    conn.close()
except sqlite3.Error as e:
    print(f"Connection failed: {e}")