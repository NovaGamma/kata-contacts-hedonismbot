import sys
import sqlite3
from pathlib import Path
from datetime import datetime


class Contacts:
    def __init__(self, db_path):
        self.db_path = db_path
        if not db_path.exists():
            print("Migrating db")
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE contacts(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
                );
              """
            )
            cursor.execute("CREATE UNIQUE INDEX index_contacts_email ON contacts(email);")
            connection.commit()
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def insert_contacts(self, contacts):
        print("Inserting contacts ...")
        cursor = self.connection.cursor()
        for name, email in contacts:
            cursor.execute(f"INSERT INTO contacts (name, email) VALUES ('{name}', '{email}')") #(?,?)garantie une insertion sécurisée des données dans la base de données.
            #print(f"Insertion de : {name}, {email}")
        self.connection.commit()

    def get_name_for_email(self, email):
        print("Looking for email", email)
        cursor = self.connection.cursor()
        start = datetime.now()
        cursor.execute(
            """
            SELECT * FROM contacts
            WHERE email = ?
            """,
            (email,),
        )
        row = cursor.fetchone()
        end = datetime.now()

        elapsed = end - start
        print("query took", elapsed.microseconds / 1000, "ms")
        if row:
            name = row["name"]
            print(f"Found name: '{name}'")
            return name
        else:
            print("Not found")


def yield_contacts(num_contacts):
    contacts = [
        ("Alice", "@domain.tld"),
        ("Bob", "@foo.com"),
        ("Charlie", "@acme.corp"),
        ("David", "@email.com"),
        ("Eve", "@example.org"),
        ("Frank", "@company.com"),
        ("Grace", "@domain.net"),
        ("Henry", "@business.io"),
        ("Ivy", "@enterprise.com"),
        ("Jack", "@startup.co"),
        # Add more contacts here...
        ]
    counter = 0
    while counter < num_contacts-1:
        name, email = contacts[counter%(len(contacts)-1)]
        email = f"{name.lower()}{counter}{email}"
        yield (name, email)
        counter += 1
    yield ("Charlie", "charlie@acme.corp")

def main():
    num_contacts = int(sys.argv[1])
    db_path = Path("contacts.sqlite3")
    contacts = Contacts(db_path)
    contacts.insert_contacts(yield_contacts(num_contacts))
    charlie = contacts.get_name_for_email("charlie@acme.corp")


if __name__ == "__main__":
    main()
