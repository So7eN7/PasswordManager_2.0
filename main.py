from tkinter import *

screen = Tk()
screen.title("Password Manager")

def loginScreen():
    screen.geometry("400x200+50+50")
    label = Label(screen, text="Enter Master Password")
    label.config(anchor=CENTER)
    label.pack()

    text = Entry(screen, width=20, show="*")
    text.pack()

    passLabel = Label(screen)
    passLabel.pack()

    def checkPassword():
        password = "password"

        if password == text.get():
            print("correct")
        else:
            passLabel.config(text="Wrong Password")

    button = Button(screen, text="Login", command=checkPassword)
    button.pack(pady=10)


loginScreen()
screen.mainloop()