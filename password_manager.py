import sys
from cryptography.fernet import Fernet
import json
import pyperclip
import password_config

key_file = password_config.key_file
password_file = password_config.password_file
initial_passwords = password_config.initial_passwords

def generate_key():
    global key_file
    key = Fernet.generate_key()
    with open(key_file, "wb") as file:
        file.write(key)


def load_key():
    return open(key_file, "rb").read()


def encrypt_password(

        password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password



def store_passwords(passwords, filename=password_file):
    encrypted_passwords = {user: encrypt_password(pw) for user, pw in passwords.items()}
    with open(filename, "w") as file:
        json.dump({user: enc_pw.decode() for user, enc_pw in encrypted_passwords.items()}, file)


def load_passwords(filename=password_file):
    with open(filename, "r") as file:
        encrypted_passwords = json.load(file)
    return {user: decrypt_password(enc_pw.encode()) for user, enc_pw in encrypted_passwords.items()}


def get_password(user, filename=password_file):
    with open(filename, "r") as file:
        encrypted_passwords = json.load(file)
    if user in encrypted_passwords:
        return decrypt_password(encrypted_passwords[user].encode())
    else:
        return None


def update_password(user, password, filename=password_file):
    try:
        with open(filename, "r") as file:
            encrypted_passwords = json.load(file)
    except FileNotFoundError:
        encrypted_passwords = {}

    encrypted_password = encrypt_password(password).decode()
    encrypted_passwords[user] = encrypted_password
    with open(filename, "w") as file:
        json.dump(encrypted_passwords, file)
    print(f"Password for {user} has been updated/added.")


def copy_passwords_to_clipboard(password):
    pyperclip.copy(password)


def pull_password_from_clipboard():
    return pyperclip.paste()


def display_users(filename=password_file):
    with open(filename, "r") as file:
        users = json.load(file).keys()
        return [user_id for user_id in users]


if __name__ == "__main__":
    operation = sys.argv[1].lower()
    if len(sys.argv) == 4:
        password=sys.argv[3]

    if operation == "start":
        answer=input("Start operation should only be done once, it will generate your secret key for encryption and decryption and create your initial json password file based on the initial_passwords dictionary. Are you sure? Y/N ").lower()
        if answer == "y":
            generate_key()
            store_passwords(initial_passwords)
        else:
            print("Okay, exiting")
            exit(0)
    elif len(sys.argv) < 3:
        print("Usage: get/put user <password>")
        exit(1)
    elif operation not in ("get", "put"):
        print(f"Argument {operation} not valid, expecting 'get' / 'put'")
        exit(1)
    elif operation == "get":
        user = sys.argv[2].lower()
        if user not in load_passwords():
            print(f"User Name {user} not found in password list, ensure password is loaded.")
            print(f"Loaded Users: {[key for key in load_passwords()]}.")
            exit(1)
        else:
            print(f"Password for {user} is {get_password(user)}, password is in your copy buffer.")
            copy_passwords_to_clipboard(get_password(user))
    elif operation == "put":
        user = sys.argv[2].lower()
        if len(sys.argv) != 4:
            print(f"Usage for put operation: <put> <user> <password>")
        elif user in load_passwords():
            if password == "clipboard":
                print(f"User name {user} found in passwords dictionary, will be updating with {pull_password_from_clipboard()} from the clipboard.")
                update_password(user, pull_password_from_clipboard())
            else:
                print(f"User name {user} found in passwords dictionary, will be updating with {password}.")
                update_password(user, password)
        else:
            if password == "clipboard":
                print(f"Adding {user}'s password {pull_password_from_clipboard()} from the clipboard.")
                update_password(user, pull_password_from_clipboard())
            else:
                print(f"Adding user name {user} password {password}.")
                update_password(user, password)