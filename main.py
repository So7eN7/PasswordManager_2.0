from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import hashlib
from database import *
import string
import random
import uuid
import os
import base64
import pyperclip
from cryptography.fernet import Fernet
#from cryptography.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

database_table = Table()
database_table.createTable()
screen = Tk()
screen.title("Password Manager")


def hashPassword(input):
    hashPass = hashlib.sha512(input)
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
    title = Label(screen, text="Password Manager", width=40, font=("Harrington", 20)).grid(columnspan=4, padx=140, pady=10)

    screenFrame = ttk.Frame(screen, padding=50)
    screenFrame.grid()
    searchBox = Entry(screenFrame, width=30, font=("Ariel", 10))
    searchBox.grid(row=3, column=1)
    searchButton = Button(screenFrame, text="Search", bg="aqua", width=20 ,font=("Ariel", 12)).grid(
        row=3, column=2, padx=5, pady=5)

    def menuLabels():
        column_num = 0
        labels = ('ID', 'Website', 'Username', 'Password')
        for label in labels:
            Label(screenFrame, text=label, bg="grey", fg="white", font=("Ariel", 12), padx=5, pady=2).grid(
                padx=5, pady=2, column=column_num, row=0)
            column_num += 1
    def userInputs():
        global user_inputs
        user_inputs = []
        column_num = 0
        for i in range(4):
            user_input = Entry(screenFrame, width=20, background="lightgray", font=("Ariel", 12))
            user_input.grid(row=1, column=column_num, padx=5, pady=2)
            column_num += 1
            user_inputs.append(user_input)

    def createButtons():
        row_num = 2
        column_num = 0
        buttons = (('Save', 'lightgreen', saveRecord), ('Update', 'lightblue', updateRecord),
                   ('Delete', 'red', deleteRecord), ('Generate', 'orange', generatePassword),
                   ('Show Records', 'midnightblue', showRecord))
        for button in buttons:
            if button[0] == "Show Records":
                column_num = 0
                row_num = 3
            Button(screenFrame, text=button[0], bg=button[1], fg="white", font=("Ariel", 12), padx=5, pady=5, width=20,
                   command=button[2]).grid(padx=5, pady=10, column=column_num, row=row_num)
            column_num += 1

    def showRecord():
        for record in record_tree.get_children():
            record_tree.delete(record)
        record_list = database_table.showRecord()
        for record in record_list:
            record_tree.insert('', END, values=(record[0], record[3], record[4], record[5]))
            # If we use 1,2 instead of 3,4,5 we will get creation dates which we don't need

    def saveRecord():
        website = user_inputs[1].get()
        username = user_inputs[2].get()
        password = user_inputs[3].get()
        record_data = {'website': website, 'username': username, 'password': password}
        database_table.createRecord(record_data)
        showRecord()
    def deleteRecord():
        ID = user_inputs[0].get()
        database_table.deleteRecord(ID)
        showRecord()
    def updateRecord():
        ID = user_inputs[0].get()
        website = user_inputs[1].get()
        username = user_inputs[2].get()
        password = user_inputs[3].get()
        record_data = {'ID': ID,'website': website, 'username': username, 'password': password}
        database_table.updateRecord(record_data)
    def recordTree():
        columns = ('ID', 'Website', 'Username', 'Password')
        global record_tree
        record_tree = ttk.Treeview(screen, columns=columns, show='headings')
        record_tree.heading('ID', text="ID")
        record_tree.heading('Website', text="Website")
        record_tree.heading('Username', text="Username")
        record_tree.heading('Password', text="Password")
        record_tree['displaycolumns'] = ('ID', 'Website', 'Username', 'Password')
        def recordSelection(event):
            for selected in record_tree.selection():
                selection = record_tree.item(selected)
                record = selection['values']
                for user_input, selection in zip(user_inputs, record):
                    user_input.delete(0, END)
                    user_input.insert(0, selection)

        record_tree.bind('<<TreeviewSelect>>', recordSelection)

        record_tree.grid()

    def generatePassword():
        # From string module we set our letters/numbers/symbols
        letters = string.ascii_letters
        numbers = string.digits
        symbols = string.punctuation
        # List comprehension really helps us here. We fill our lists here
        password_letters = [random.choice(letters) for i in range(random.randint(8, 10))]
        password_numbers = [random.choice(numbers) for i in range(random.randint(2, 4))]
        password_symbols = [random.choice(symbols) for i in range(random.randint(2, 4))]
        # Combining our lists and shuffling them
        password_list = password_letters + password_numbers + password_symbols
        random.shuffle(password_list)
        # Make a string and put it inside the password box
        password = "".join(password_list)
        user_inputs[3].insert(0, password)

    menuLabels()
    userInputs()
    createButtons()
    recordTree()

cursor.execute("SELECT * FROM master_password")
if cursor.fetchall():
    loginScreen()
else:
    firstLogin()
screen.mainloop()