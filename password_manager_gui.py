from tkinter import *
import password_manager

# -------------- Test Zone ------------- #

users_list = password_manager.display_users()

# -------------- UI SETUP -------------- #

root = Tk()
users_list_var = StringVar(root,users_list)
root.title("Password Manager")
root.config(padx=50, pady=50)
root.minsize(width=500, height=500)


user = StringVar()
user.set("User Name")
user_entry = Entry(root, textvariable=user)
user_entry.pack()

password = StringVar()
password.set("Password")
password = Entry(root, textvariable=password)
password.pack()

# pw_listbox = Listbox(root, height=10, listvariable=users_list_var)
# pw_listbox.pack()

root.mainloop()