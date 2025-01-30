from database_manager import *
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    add_contact_to_database(Contact("John", "Doe", "123-456-7890", "john.doe@example.com", "123 Main St, Anytown", "Friend from college"))
    add_contact_to_database(Contact("Jane", "Smith", "987-654-3210", "jane.smith@work.com", "456 Oak Ave, Otherville", "Work colleague"))
    add_contact_to_database(Contact("Alice", "Johnson", "555-123-4567", "alice.j@personal.net", "789 Pine Ln, Somewhere", "Family member"))
    add_contact_to_database(Contact("Bob", "Williams", "111-222-3333", "bob.w@email.org", "101 Elm Rd, Nowhere", "Gym buddy"))
    add_contact_to_database(Contact("Charlie", "Brown", "444-555-6666", "charlie.b@mail.com", "222 Maple Dr, Thisplace", "Childhood friend"))

    app.run(debug=True)
