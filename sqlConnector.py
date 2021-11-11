import mysql.connector
from dotenv import load_dotenv
import os


class sqlConnector():

    def __init__(self):
        load_dotenv()
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        self.conn = mysql.connector.connect(username=username, password=password, host='localhost')
        self.cursor = self.conn.cursor()

    def createDatabase(self, name):
        self.cursor.execute("Drop Database If Exists {}".format(name))
        self.cursor.execute("Create database {}".format(name))
        self.cursor.execute("Use {}".format(name))

    def create_table(self, name, attributes):
        self.cursor.execute("Create table {} ({})".format(name, ','.join(attributes)))

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_into_table(self, name, values):
        self.cursor.execute("Insert into {} VALUES ({})".format(name, ','.join(values)))

    def commit(self):
        self.conn.commit()
