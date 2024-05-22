#Password Management Application

Basic password management utility that ideally runs in a Windows environment to be paired with AutoHotKey; would work fine in Linux/Mac, just without the hotkey functionality.

The utility will ingest your passwords either via a dictionary in the script (recommended for initial load only), or via a "put" command. The passwords are encrypted and saved into a .json file. When you want to retrieve the passwords, you can execute a "get" command which will output the decrypted password into the terminal as well as copying it into your clipboard.

Requirements:
    1. Python Installed.
    2. Additional Python Libraries cryptography and pyperclip. 
    3. AutoHotKey installed for shortcut hotkeys to be enabled.

First Time Use:
    1. Save password_manager.py and password_copy.ahk into the same directory on your PC.
    2. Populate the dictionary named 'intial_passwords' in the script password_manager.py. You can add more later, but this will save you some time instead of adding the passwords one at a time later.
    3. Update the key_file and password_file variables to the directory and files you want your key file and passwords file saved.
    4. Execute the script with only the 'start' argument; python password_manager.py start. This builds out your initial secret key and encrypted password file from the dictionary saved in the script.

Ongoing Use:
    1. Usage: "python password_manager.py put user password". 
        This will insert the new user and password into the json file. If the user already exists, it will update the existing password.
    2. Usage: "python password_manager.py get user"
        This will retrieve and decrypt the password saved for the user, and output it to the terminal. The password will also be stored in the clipboard.

AutoHotKey Component (Windows Only):
    1. Install AutoHotKey (https://www.autohotkey.com/). If installed for current user only, did not require adminisrator privileges.
    2. Update password_copy.ahk script with your user IDs. Shortcuts set to Alt+p for aa-a, Alt+q for q_aa, and Alt+d for d_aa.
    2. Execute the password_copy.ahk script. This will create a process on your PC that constantly runs, allowing you to use the hotkey shortcuts. It can be viewed in the control panel on the bottom right.
    3. If you want this to automatically kick off on the start of your PC, go to your Run dialog, type "shell:startup", and then place a shortcut to password_copy.ahk into that directory.

