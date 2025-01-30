import sqlite3
from mistralai import Mistral
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

DATABASE_NAME = 'contacts.db'
API_KEY = os.getenv("MISTRAL_API_KEY")
SIMILARITY_THRESHOLD = 0.7

class Contact:
    def __init__(self, first_name, last_name, phone, email, address, notes, contact_id=None):
        self.contact_id = contact_id
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

def delete_contact_from_database(contact_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM contacts WHERE id = ?''', (contact_id,))
    conn.commit()
    conn.close()

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    return dot_product / (norm_vec1 * norm_vec2)

def search_contact_in_database(query):
    print(f"Searching for query: '{query}'") # Print the search query
    if not API_KEY:
        raise ValueError("MISTRAL_API_KEY environment variable not set. Cannot perform semantic search.")

    client = Mistral(api_key=API_KEY)
    print("Mistral Client initialized successfully.") # Check client initialization

    query_embedding = None # Initialize outside try block
    try:
        query_embedding_response = client.embeddings(model="mistral-embed", input=[query])
        query_embedding = query_embedding_response.data[0].embedding.vector
        print(f"Query embedding generated successfully. Embedding length: {len(query_embedding) if query_embedding else 'None'}") # Check query embedding
    except Exception as e:
        print(f"Error generating embedding for query: {e}")
        return []

    if query_embedding is None: # Check if embedding generation failed
        print("Query embedding is None, cannot proceed with search.")
        return []

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    print(f"Fetched {len(rows)} contacts from the database.") # Check fetched contacts

    results = []
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

        contact_text_for_embedding = f"{contact.first_name} {contact.last_name} {contact.notes}"
        print(f"Generating embedding for contact: {contact.first_name} {contact.last_name}, Text: '{contact_text_for_embedding}'") # Check contact text

        contact_embedding = None # Initialize outside try block
        try:
            contact_embedding_response = client.embeddings(model="mistral-embed", input=[contact_text_for_embedding])
            contact_embedding = contact_embedding_response.data[0].embedding.vector
            print(f"Contact embedding generated successfully. Embedding length: {len(contact_embedding) if contact_embedding else 'None'}") # Check contact embedding
        except Exception as e:
            print(f"Error generating embedding for contact {contact.contact_id}: {e}")
            continue

        if contact_embedding is None: # Check if embedding generation failed
            print(f"Contact embedding for {contact.contact_id} is None, skipping similarity calculation.")
            continue


        similarity = cosine_similarity(query_embedding, contact_embedding)
        print(f"Similarity between query and contact {contact.contact_id}: {similarity}") # Check similarity score

        if similarity > SIMILARITY_THRESHOLD:
            print(f"Contact {contact.contact_id} is above threshold ({SIMILARITY_THRESHOLD}), adding to results.") # Check threshold condition
            results.append((contact, similarity))
        else:
            print(f"Contact {contact.contact_id} is below threshold ({SIMILARITY_THRESHOLD}).") # Check threshold condition

    results.sort(key=lambda x: x[1], reverse=True)
    print(f"Returning {len(results)} search results.") # Check number of results

    return [contact for contact, similarity in results]