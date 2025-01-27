import sqlite3
import tkinter as tk
from database_manager import *
from constants import DATABASE_NAME

class Contact:
    def __init__(self, first_name, last_name, phone, email, address, notes):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes


def add_contact_to_database(contact):
    pass

if __name__ == "__main__":  # Just for testing
    create_database_table()
    window = tk.Tk()
    window.title("Contacts Pro")
    window.mainloop()
