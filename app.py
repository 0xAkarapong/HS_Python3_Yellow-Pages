from database_manager import *
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', contacts=get_all_contacts_from_database())

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        contact = Contact(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            phone=request.form['phone'],
            email=request.form['email'],
            address=request.form['address'],
            notes=request.form['notes']
        )
        if not contact.first_name:
            error = "First Name is required."
            return render_template('add_contact.html', error=error) 

        new_contact = contact
        add_contact_to_database(new_contact)
        return redirect(url_for('home')) 

    return render_template('add_contact.html')

@app.route('/delete/<int:contact_id>')
def delete_contact(contact_id):
    delete_contact_from_database(contact_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    create_database_table()
    app.run(debug=True)
