from tkinter import *

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
            pass
        else:
            errorLabel.config(text="Passwords do not match")

    button = Button(screen, text="Login", command=savePassword)
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

    def checkPassword():
        password = "password"

        if password == passEntry.get():
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
firstLogin()
screen.mainloop()