import sys
import os
from cryptography.fernet import Fernet
import json
import pyperclip


# config_dir = "/Users/masonfrance/Projects/PasswordManagement/"
config_dir = "/pw_config/"
key_file = rf"{config_dir}secret.key"
password_file = rf"{config_dir}passwords.json"

"""
#TODO 2. In the init block, if we blindly generate a new key while having an existing passwords file lingering, we won't be able to decrypt. May need to give a warning and if approved, generate new key and create new blank file?
#TODO 3. Add delete functionality.
"""


def first_time_initialize():
    make_dirs()
    create_empty_file()
    generate_key()


def make_dirs():
    os.makedirs(config_dir, exist_ok=True)


def create_empty_file():
    open(password_file, "a").close()


def check_key_file():
    return os.path.isfile(key_file)


def check_password_file():
    return os.path.isfile(password_file)


def generate_key():
    global key_file
    key = Fernet.generate_key()
    with open(key_file, "wb") as file:
        file.write(key)


def load_key():
    read_key = open(key_file, "rb").read()
    return read_key


def encrypt_password(password_to_encrypt):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password_to_encrypt.encode())
    return encrypted_password


def decrypt_password(password_to_decrypt):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(password_to_decrypt).decode()
    return decrypted_password


def check_passwords():
    with open(password_file, "r") as file:
        encrypted_passwords = json.load(file)
    return {stored_user: decrypt_password(enc_pw.encode()) for stored_user, enc_pw in encrypted_passwords.items()}


def get_password(requested_user):
    with open(password_file, "r") as file:
        encrypted_passwords = json.load(file)
    if requested_user in encrypted_passwords:
        return decrypt_password(encrypted_passwords[requested_user].encode())
    else:
        return None


def update_password(user_input, user_password):
    with open(password_file, "r") as file:
        encrypted_passwords = json.load(file)
    encrypted_password = encrypt_password(user_password).decode()
    encrypted_passwords[user_input] = encrypted_password
    with open(password_file, "w") as file:
        json.dump(encrypted_passwords, file)


def copy_passwords_to_clipboard(password_to_copy):
    pyperclip.copy(password_to_copy)


def pull_password_from_clipboard():
    return pyperclip.paste()


def display_users():
    with open(password_file, "r") as file:
        users = json.load(file).keys()
        return [user_id for user_id in users]


"""
Input Options:
python script.py get <user>

python script.py put <user> <password>

python script.py put <user> clipboard
"""

if __name__ == "__main__":
    init = True
    while init:
        if not check_key_file():
            answer = input(f"Key file not found. Check configuration and README.md. If this is your first run, can we create in default directory {config_dir}? Y/N ").lower()
            if answer == "y":
                make_dirs()
                generate_key()
            else:
                print("Key required for use, exiting.")
                exit(1)
        elif not check_password_file():
            answer = input(f"Password file not found. Check configuration and README.md. If this is your first run, we can create in default directory {config_dir}? Y/N ").lower()
            if answer == "y":
                make_dirs()
                create_empty_file()
            else:
                print("Password file required for use, exiting.")
                exit(1)
        else:
            init = False
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ("get", "put"):
        print("Usage: get/put user <password>|clipboard")
    elif sys.argv[1].lower() == "get":
        try:
            user = sys.argv[2].lower()
        except IndexError:
            print("User required for get operation. Usage: get/put user <password>|clipboard")
        else:
            if user not in check_passwords():
                print(f"User Name {user} not found in password list, ensure password is loaded.")
                print(f"Loaded Users: {[key for key in check_passwords()]}.")
                exit(1)
            else:
                print(f"Password for {user} is {get_password(user)}, password is in your copy buffer.")
                copy_passwords_to_clipboard(get_password(user))
    elif sys.argv[1].lower() == "put":
        try:
            user = sys.argv[2].lower()
            password = sys.argv[3].lower()
        except IndexError:
            print("User and password required for put operation. Usage: get/put user <password>|clipboard")
        else:
            if password == "clipboard":
                print(f"Updating {user} with password {pull_password_from_clipboard()} from the clipboard.")
                update_password(user, pull_password_from_clipboard())
            else:
                print(f"Updating {user} with {password}.")
                update_password(user, password)
    else:
        print("End of loop")
