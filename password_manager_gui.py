from tkinter import *
import password_manager
from tkinter import messagebox

# -------------- Test Zone ------------- #

users_list = password_manager.display_users()


# -------------- FUNCTIONS ------------- #

# Check if key/password file are present; if not, offer to create.
def check_program_init():
    pass


def get_password_from_list():
    input_user = pw_listbox.get(pw_listbox.curselection())
    output_password = password_manager.get_password(input_user)
    messagebox.showinfo(title="Password", message=f"User: {input_user}\nPassword: {output_password}")


def add_password_to_file():
    pass


# -------------- UI SETUP -------------- #

# Main Window
root = Tk()
root.title("Password Manager")
root.config(padx=50, pady=50)
root.minsize(width=500, height=500)


# Label for Update Functions

update_label = Label(text="Add or Update Passwords")
update_label.grid(column=0, row=0, sticky="n")

# UserName Entry
user = StringVar()
user.set("User Name")
user_entry = Entry(root, textvariable=user)
user_entry.grid(column=0, row=1, sticky="sw")

# Password Entry
password = StringVar()
password.set("Password")
password = Entry(root, textvariable=password)
password.grid(column=0, row=2, sticky="sw")

update_password_button = Button(root, text="Update Password", width=25, command=add_password_to_file)
update_password_button.grid(column=0, row=3, sticky="w")

# Label for Find functions

get_password_label = Label(root, text="Retrieve Passwords")
get_password_label.grid(column=1, row=0, sticky="n")

# Existing Users List
users_list_var = StringVar(root, users_list)
pw_listbox = Listbox(root, height=10, listvariable=users_list_var, selectmode="single", width=30)
pw_listbox.grid(column=1, row=2, sticky="w")

# Get Password button from Users List
get_button = Button(text="Get Password", command=get_password_from_list, width=25)
get_button.grid(column=1, row=3)


root.mainloop()
