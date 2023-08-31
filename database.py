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

