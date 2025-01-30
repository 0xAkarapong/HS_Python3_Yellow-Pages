import sqlite3
from faker import Faker

# Your database setup (replace with your actual database name and Contact class)
DATABASE_NAME = 'contacts.db'

class Contact:
    def __init__(self, first_name, last_name, phone, email, address, notes):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes

def add_contact_to_database(contact: Contact) -> int:
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contacts (first_name, last_name, phone, email, address, notes)
                VALUES (?,?,?,?,?,?)
            ''', (contact.first_name, contact.last_name, contact.phone, contact.email, contact.address, contact.notes))
            contact_id = cursor.lastrowid
            conn.commit()
            return contact_id
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return -1

# Generate and insert 50 fake contacts
if __name__ == "__main__":
    fake = Faker()
    for _ in range(50):
        contact = Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            email=fake.email(),
            address=fake.street_address(),
            notes=fake.sentence()
        )
        add_contact_to_database(contact)
    print("Added 50 fake contacts to the database.")