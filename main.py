from tkinter import *
from tkinter import messagebox
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

screen = Tk()
screen.title("Password Manager")


def firstLogin():
    screen.geometry("400x200+50+50")
    label = Label(screen, text="Create Master Password")
    label.config(anchor=CENTER)
    label.pack()

    passEntry = Entry(screen, width=20)
    passEntry.focus()
    passEntry.pack()

    repeatLabel = Label(screen, text="Repeat Password")
    repeatLabel.pack()

    repeatEntry = Entry(screen, width=20)
    repeatEntry.pack()
    repeatEntry.focus()

    errorLabel = Label(screen)
    errorLabel.pack()

    def savePassword():
        if passEntry.get() == repeatEntry.get():
            passwordHash = passEntry.get()
            passwordInput = """INSERT INTO master_password(password) VALUES(?)"""
            cursor.execute(passwordInput, [(passwordHash)])
            db.commit()
            messagebox.showinfo(title="Success!", message="Password created successfully, please restart the app")
        else:
            errorLabel.config(text="Passwords do not match")

    button = Button(screen, text="Create", command=savePassword)
    button.pack(pady=10)

def loginScreen():
    screen.geometry("400x200+50+50")
    label = Label(screen, text="Enter Master Password")
    label.config(anchor=CENTER)
    label.pack()

    passEntry = Entry(screen, width=20, show="*")
    passEntry.focus()
    passEntry.pack()

    passLabel = Label(screen)
    passLabel.pack()

    def getMasterPassword():
        masterHashChecking = passEntry.get()
        cursor.execute("SELECT * FROM master_password WHERE id = 1 and password = ?", [(masterHashChecking)])
        return cursor.fetchall()
    def checkPassword():
        passCheck = getMasterPassword()

        if passCheck:
            mainScreen()
        else:
            passEntry.delete(0, 'end')
            passLabel.config(text="Wrong Password")

    button = Button(screen, text="Login", command=checkPassword)
    button.pack(pady=10)

def mainScreen():

    for widget in screen.winfo_children():
        widget.destroy()

    screen.geometry("800x500+50+50")
    label = Label(screen, text="Password Manager", pady=20, font=("Arial", 20))
    label.grid(row=0, column=0, padx=280)

'''
    add = Button(text="Add")
    add.grid(row=1, column=1)
    delete = Button(text="Delete")
    delete.grid(row=1, column=2)
    generatePassword = Button(text="Generate Password")
    generatePassword.grid(row=1, column=3)
'''


cursor.execute("SELECT * FROM master_password")
if cursor.fetchall():
    loginScreen()
else:
    firstLogin()
screen.mainloop()