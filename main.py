from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import hashlib
from database import *


database_table = Table()
database_table.createTable()
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

    def saveRecord():
        website = user_inputs[1].get()
        username = user_inputs[2].get()
        password = user_inputs[3].get()
        record_data = {'website': website, 'username': username, 'password': password}
        database_table.createRecord(record_data)
    def deleteRecord():
        pass
    def updateRecord():
        pass
    def showRecord():
        record_list = database_table.showRecord()
        for record in record_list:
            print(record)
    def generatePassword():
        pass

    menuLabels()
    userInputs()
    createButtons()

cursor.execute("SELECT * FROM master_password")
if cursor.fetchall():
    loginScreen()
else:
    firstLogin()
screen.mainloop()