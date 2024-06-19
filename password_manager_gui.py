from tkinter import *
import password_manager
from tkinter import messagebox


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
    password_manager.update_password(user_button, password_button)
    if user_button in existing_users:
        messagebox.showinfo(title="Update Succeeded", message=f"User: {user_button} successfully updated")
    else:
        pw_listbox.insert(END, user_button)
        messagebox.showinfo(title="Add Succeeded", message=f"User: {user_button} successfully added")


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
user_entry.grid(column=0, row=2, sticky="nw")

# Password Entry
password = StringVar()
password.set("Password")
password_entry = Entry(root, textvariable=password)
password_entry.grid(column=0, row=2, sticky="sw")

update_password_button = Button(root, text="Update Password", width=25, command=add_password_to_file)
update_password_button.grid(column=0, row=3, sticky="w")

# Label for Find functions

get_password_label = Label(root, text="Retrieve Passwords")
get_password_label.grid(column=1, row=0, sticky="n")

# Existing Users List
users_list = password_manager.display_users()
users_list_var = StringVar(root, users_list)
pw_listbox = Listbox(root, height=10, listvariable=users_list_var, selectmode="single", width=30)
pw_listbox.grid(column=1, row=2, sticky="w")

# Get Password button from Users List
get_button = Button(text="Get Password", command=get_password_from_list, width=25)
get_button.grid(column=1, row=3)

if check_program_init:
    messagebox.showinfo(title="Initialize Complete", message="Key and Password Files Detected.")
else:
    if messagebox.askyesno(title="Initialize Needed.", message="No Key and Password File Detected.\nNeed to generate "
                                                               "files.\nWarning: This will results in older files no "
                                                               "longer working."):
        password_manager.first_time_initialize()
    else:
        print("No")

root.mainloop()
