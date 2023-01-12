"""
A simple Flask web application for listing charities and social services in Medford.
Data is stored in a SQLite database that looks something like the following:

+------------------+----------------------------------+------------------+------------------+------------------+--------------------+------------------+
| name             | description                      | street_address   | type_of_service  | phone_number     | hours_of_operation | reviews          |
+------------------+----------------------------------+------------------+------------------+------------------+--------------------+------------------+
| Giving Hands     | provides for families in need    | 123 Main Street  | charity          | 541-555-1234     | 4:00pm-8:00pm      |                  |
+------------------+----------------------------------+------------------+------------------+------------------+--------------------+------------------+

This can be created with the following SQL (see bottom of this file):

create table charities (name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews)

"""
from datetime import date
from .Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from charities")
        except sqlite3.OperationalError:
            cursor.execute("create table charities (name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM charities")
        return cursor.fetchall()

    def insert(self, name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews):
        """
        Inserts entry into database
        :param name: String
        :param description: String
        :param street_address: String
        :param type_of_service: String
        :param phone_number: String
        :param hours_of_operation: String
        :param reviews: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'name':name, 'description':description, 'street_address':street_address, 'type_of_service':type_of_service,
                  'phone_number':phone_number, 'hours_of_operation':hours_of_operation, 'reviews':reviews}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("""insert into charities (name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews)
        VALUES (:name, :description, :street_address, :type_of_service, :phone_number, :hours_of_operation, :reviews)""", params)

        connection.commit()
        cursor.close()
        return True
