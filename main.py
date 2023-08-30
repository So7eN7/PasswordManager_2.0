from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import hashlib
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


def hashPassword(input):
    hashPass = hashlib.md5(input)
    hashPass = hashPass.hexdigest()
    return hashPass

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
            passwordHash = hashPassword(passEntry.get().encode('utf-8'))
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
        masterHashChecking = hashPassword(passEntry.get().encode('utf-8'))
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

    screen.geometry("900x600+50+50")
    title = Label(screen, text="Password Manager", width=40, font=("Ariel", 20)).grid(columnspan=4, padx=140, pady=10)

    screenFrame = ttk.Frame(screen, padding=50)
    screenFrame.grid()

    def menuLabels():
        column_num = 0
        labels = ('ID', 'Website', 'Username', 'Password')
        for label in labels:
            Label(screenFrame, text=label, bg="grey", fg="white", font=("Ariel", 12), padx=5, pady=2).grid(
                padx=5, pady=2, column=column_num, row=0)
            column_num += 1
    def userInputs():
        user_inputs = []
        column_num = 0
        for i in range(4):
            user_input = Entry(screenFrame, width=20, background="lightgray", font=("Ariel", 12))
            user_input.grid(row=1, column=column_num, padx=5, pady=2)
            column_num += 1
            user_inputs.append(user_input)

    def createButtons():
        column_num = 0
        buttons = (('Save', 'lightgreen'), ('Update', 'lightblue'), ('Delete', 'red'), ('Generate', 'orange'))
        for button in buttons:
            Button(screenFrame, text=button[0], bg=button[1], fg="white", font=("Ariel", 12), padx=5, pady=2, width=20).grid(
                padx=5, pady=2, column=column_num, row=2)
            column_num += 1

    menuLabels()
    userInputs()
    createButtons()

cursor.execute("SELECT * FROM master_password")
if cursor.fetchall():
    loginScreen()
else:
    firstLogin()
screen.mainloop()