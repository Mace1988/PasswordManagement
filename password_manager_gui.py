from tkinter import *
import password_manager
from tkinter import messagebox
# -------------- Test Zone ------------- #

users_list = password_manager.display_users()


# -------------- FUNCTIONS ------------- #

def get_password_from_list():
    user = pw_listbox.get(pw_listbox.curselection())
    password = password_manager.get_password(user)
    messagebox.showinfo(title="Password", message=f"User: {user}\nPassword: {password}")


# -------------- UI SETUP -------------- #

root = Tk()
users_list_var = StringVar(root, users_list)
root.title("Password Manager")
root.config(padx=50, pady=50)
root.minsize(width=500, height=500)

user = StringVar()
user.set("User Name")
user_entry = Entry(root, textvariable=user)
user_entry.grid(column=0, row=1, sticky="w")

password = StringVar()
password.set("Password")
password = Entry(root, textvariable=password)
password.grid(column=0, row=2, sticky="w")

get_button = Button(text="Get", command=get_password_from_list)
get_button.grid(column=2, row=3, sticky="w")

pw_listbox = Listbox(root, height=10, listvariable=users_list_var, selectmode="single")
pw_listbox.grid(column=2, row=2, sticky="w")

root.mainloop()
