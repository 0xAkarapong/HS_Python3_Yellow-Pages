import sqlite3
import tkinter as tk
from database_manager import *
from constants import *

if __name__ == "__main__":  # Just for testing
    create_database_table()
    window = tk.Tk()
    window.title("Contacts Pro")
    window.mainloop()
