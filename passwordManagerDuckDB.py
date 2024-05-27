import sys
from cryptography.fernet import Fernet
import json
import pyperclip
import duckdb

key_file=r"C:\Users\a673538\OneDrive - Bread Financial\Documents\Scripts\Python\PasswordManagement\secret.key"
# password_file=r"C:\Users\a673538\OneDrive - Bread Financial\Documents\Scripts\Python\PasswordManagement\passwords.json"
db_file="/Users/masonfrance/Projects/PasswordManagement"

#Only used during start operation, should populate with your intial list of passwords to save time.
intial_passwords = {
    "d_aa-a673538": "8=LQbWVLAYvtqu/d",
    "q_aa-a673538": "jsAb!JUmO2/IyCae",
    "aa-a673538": "h6Lru/epx85i2j0x"
}

#No change
def generate_key():
    key = Fernet.generate_key()
    with open(key_file, "wb") as key_file:
        key_file.write(key)

#No Change
def load_key():
    return open(key_file, "rb").read()

#No Change
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

#No Change
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

#TODO 1. Need to create the duckdb instance written to a file we'll store in github.

#TODO 2. Need to convert this to write into the duckdb
# Can pass in a dictionary of intial passwords, will create the encryped passwords file.
def store_passwords(passwords, filename=password_file):
    encrypted_passwords = {user: encrypt_password(pw) for user, pw in passwords.items()}
    with open(filename, "w") as file:
        json.dump({user: enc_pw.decode() for user, enc_pw in encrypted_passwords.items()}, file)

#TODO 3. Should open the duckdb and return decrypted values from that
# Used to view all decryped passwords. Output is a dictionary.
def load_passwords(filename=password_file):
    with open(filename, "r") as file:
        encrypted_passwords = json.load(file)
    return {user: decrypt_password(enc_pw.encode()) for user, enc_pw in encrypted_passwords.items()}

#TODO 4. Should open the duckdb and return decrypted value from that
def get_password(user, filename=password_file):
    with open(filename, "r") as file:
        encrypted_passwords = json.load(file)
    if user in encrypted_passwords:
        return decrypt_password(encrypted_passwords[user].encode())
    else:
        return None

#TODO 5. Open and update the duckdb instead of recreating file.
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


operation=sys.argv[1].lower()
user=sys.argv[2].lower()
if len(sys.argv)==4:
    password=sys.argv[3]

if operation == "start":
    answer=input("Start operation should only be done once, it will generate your secret key for encryption and decryption and create your initial json password file based on the initial_passwords dictionary. Are you sure? Y/N").lower()
    if answer=="Y":
        generate_key()
        store_passwords(intial_passwords)
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
    if user not in load_passwords():
        print(f"User Name {user} not found in password list, ensure password is loaded.")
        print(f"Loaded Users: {[key for key in load_passwords()]}")
        exit(1)
    else:
        print(f"Password for {user} is {get_password(user)}, password is in your copy buffer.")
        copy_passwords_to_clipboard(get_password(user))
elif operation == "put":
    if len(sys.argv) != 4:
        print(f"Usage for put operation: <put> <user> <password>")
    elif user in load_passwords():
        print(f"User name {user} found in passwords dictionary, will be updating with {password}")
        update_password(user, password)
    else:
        print(f"Adding {user}'s password {password} to dictionary")
        update_password(user, password)