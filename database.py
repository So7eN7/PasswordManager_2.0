import sqlite3

with sqlite3.connect("password_manager.db") as db:
    cursor = db.cursor()

cursor.execute\
("""
CREATE TABLE IF NOT EXISTS master_password
(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL
);
""")

class Table:

    def connect(self):
        connection = sqlite3.connect('password_manager.db')
        return connection

    def createTable(self, table_name="password_record"):
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
        )
        '''
        with connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
