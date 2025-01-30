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

def add_contact_to_database(contact: Contact) -> int:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO contacts (first_name, last_name, phone, email, address, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (contact.first_name, contact.last_name, contact.phone, contact.email, contact.address, contact.notes))
    conn.commit()
    contact_id = cursor.lastrowid
    conn.close()
    return contact_id


def get_all_contacts_from_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()

    contacts = []
    for row in rows:
        contact = Contact(
            contact_id=row[0],
            first_name=row[1],
            last_name=row[2],
            phone=row[3],
            email=row[4],
            address=row[5],
            notes=row[6]
        )
        contacts.append(contact)
    return contacts

def update_contact_in_database(contact):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE contacts SET
            first_name = ?,
            last_name = ?,
            phone = ?,
            email = ?,
            address = ?,
            notes = ?
        WHERE id = ?
    ''', (contact.first_name, contact.last_name, contact.phone, contact.email, contact.address, contact.notes, contact.contact_id))
    conn.commit()
    conn.close()

def delete_contact_from_database(contact):
    conn = sqlite3.connect(DATABASE_NAME)
    pass

def search_contact_in_database(contact):
    conn = sqlite3.connect(DATABASE_NAME)
    pass