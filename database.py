import sqlite3

# Setting up our database
with sqlite3.connect("password_manager.db") as db:
    cursor = db.cursor()

# Storing our data
cursor.execute\
("""
CREATE TABLE IF NOT EXISTS master_password
(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
authentication_key TEXT NOT NULL
);
""")

class Table:

    def connect(self):  # Connecting to our database
        connection = sqlite3.connect('password_manager.db')
        return connection

    def createTable(self, table_name="password_record"):  # Creating the table to store our data #2
        connection = self.connect()
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name}
        (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        website TEXT NOT NULL,
        username VARCHAR(100) DEFAULT NULL,
        password VARCHAR(100) DEFAULT NULL
        );
        '''
        with connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)

    def showRecord(self, table_name="password_record"):  # Showing the records
        connection = self.connect()  # Connect to the database and show
        query = f'''
                SELECT * FROM {table_name} 
                '''
        with connection as connection:
            cursor = connection.cursor()
            record_list = cursor.execute(query)
            return record_list

    def createRecord(self, record_data, table_name="password_record"):  # Creating the records
        website = record_data['website']
        username = record_data['username']
        password = record_data['password']
        connection = self.connect()  # Getting the inputs and inserting them into the database
        query = f'''
                INSERT INTO {table_name} ('website', 'username', 'password') VALUES ( ?, ?, ? );
                '''
        with connection as connection:
            cursor = connection.cursor()
            cursor.execute(query, (website, username, password))

    def updateRecord(self, record_data, table_name="password_record"):  # Same as the function above + ID
        ID = record_data['ID']
        website = record_data['website']
        username = record_data['username']
        password = record_data['password']
        connection = self.connect()
        query = f'''
                UPDATE {table_name} SET website = ?, username = ?, password = ? WHERE ID = ?;
                '''
        with connection as connection:
            cursor = connection.cursor()
            cursor.execute(query, (website, username, password, ID))

    def deleteRecord(self, ID, table_name="password_record"):  # Delete the records
        connection = self.connect()  # Delete the record based on the ID
        query = f'''
                DELETE  FROM {table_name} WHERE ID = ?;
                '''
        with connection as connection:
            cursor = connection.cursor()
            cursor.execute(query, (ID,))