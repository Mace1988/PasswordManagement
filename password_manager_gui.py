from tkinter import *
from tkinter import messagebox

import customtkinter
from customtkinter import *
import password_manager


FONT = ("roboto", 16)
FG_LABEL = "black"
BG_LABEL = "grey"
FG_BUTTON = "black"
BG_BUTTON = "grey"


def check_program_init():
    if password_manager.check_password_file() and password_manager.check_key_file():
        return True
    else:
        return False


def get_password_from_list():
    input_user = pw_listbox.get(pw_listbox.curselection())
    output_password = password_manager.get_password(input_user)
    messagebox.showinfo(title="Password", message=f"User: {input_user}\nPassword: {output_password}")


def add_password_to_file():
    existing_users = password_manager.display_users()
    user_button = user_entry.get()
    password_button = password_entry.get()
    if user_button == "User Name" or password_button == "Password":
        messagebox.showinfo(title="Default Value Error", message="Please do not pass default values.")
    else:
        password_manager.update_password(user_button, password_button)
        if user_button in existing_users:
            messagebox.showinfo(title="Update Succeeded", message=f"User: {user_button} successfully updated")
        else:
            pw_listbox.insert(END, user_button)
            messagebox.showinfo(title="Add Succeeded", message=f"User: {user_button} successfully added")


def delete_user():
    input_user = pw_listbox.get(pw_listbox.curselection())
    print(input_user)
    password_manager.delete_user(input_user)
    idx = pw_listbox.get(0, END).index(input_user)
    pw_listbox.delete(idx)
    messagebox.showinfo(title="Delete Succeeded", message=f"User: {input_user} successfully removed.")

# -------------- UI SETUP -------------- #


# Main Window
root = CTk()
root.title("Password Manager")
root.config(padx=50, pady=50)
root.minsize(width=500, height=500)

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")
# Frame to show initialization status


init_label = CTkLabel(root, text="", font=FONT, padx=20, pady=20)
init_label.grid(column=0, row=0, columnspan=3, sticky="n")

instruction_label = CTkLabel(root, text="Passwords can be added below by inputting the username and password. You can also update an existing password in the same way.", padx=20, pady=20, font=("roboto", 12), wraplength=160)
instruction_label.grid(column=0, row=1, rowspan=4)
# Label for Update Functions

update_label = CTkLabel(root, text="Input", font=FONT)
update_label.grid(column=0, row=1)

# UserName Entry
user = StringVar()
user.set("User Name")
user_entry = CTkEntry(root, textvariable=user)
user_entry.grid(column=0, row=7, sticky="sw", padx=5, pady=5)

# Password Entry
password = StringVar()
password.set("Password")
password_entry = CTkEntry(root, textvariable=password)
password_entry.grid(column=0, row=8, sticky="sw", padx=5, pady=5)

update_password_button = CTkButton(root, text="Add User/Update Password", width=25, command=add_password_to_file)
update_password_button.grid(column=0, row=9, sticky="w")

# Label for Find functions

retrieve_password_label = CTkLabel(root, text="User List", font=FONT)
retrieve_password_label.grid(column=1, row=1, sticky="n", columnspan=2)

# Existing Users List
users_list = password_manager.display_users()
users_list_var = StringVar(root, users_list)
pw_listbox = Listbox(root, height=10, listvariable=users_list_var, selectmode="single", width=30)
pw_listbox.grid(column=1, row=2, sticky="n", columnspan=2)

# Get Password button from Users List
get_button = CTkButton(root, text="Get Password", command=get_password_from_list, width=15)
get_button.grid(column=1, row=9)

delete_button = CTkButton(root, text="Delete User", command=delete_user, width=15)
delete_button.grid(column=2, row=9
                   )
if check_program_init:
    init_label.configure(text="Initialization Complete ✅")
else:
    if messagebox.askyesno(title="Initialize Needed.", message="No Key and Password File Detected.\nNeed to generate "
                                                               "files.\nWarning: This will results in older files no "
                                                               "longer working."):
        password_manager.first_time_initialize()
    else:
        print("No")


root.mainloop()
