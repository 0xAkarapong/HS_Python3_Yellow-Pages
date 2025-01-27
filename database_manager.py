from constants import *
import sqlite3

class Contact:
    def __init__(self, first_name, last_name, phone, email, address, notes):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes

def create_database_table() :
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                notes TEXT
            )
        ''')
    conn.commit()
    conn.close()

def add_contact_to_database(contact):
    pass

def get_all_contacts_from_database():
    pass

def update_contact_in_database(contact):
    pass

def delete_contact_from_database(contact):
    pass

def search_contact_in_database(contact):
    pass