from tkinter import *

screen = Tk()
screen.title("Password Manager")



def loginScreen():
    screen.geometry("400x200+50+50")
    label = Label(screen, text="Enter Master Password")
    label.config(anchor=CENTER)
    label.pack()

    text = Entry(screen, width=20, show="*")
    text.focus()
    text.pack()

    passLabel = Label(screen)
    passLabel.pack()

    def checkPassword():
        password = "password"

        if password == text.get():
            mainScreen()
        else:
            text.delete(0, 'end')
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
loginScreen()
screen.mainloop()