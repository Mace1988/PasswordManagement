import sys
from cryptography.fernet import Fernet
import json
import pyperclip


key_file = r"/Users/masonfrance/Projects/PasswordManagement/secret.key"
password_file = r"/Users/masonfrance/Projects/PasswordManagement/passwords.json"

#TODO 2. Remove initial passwords population functionality. Complicates the code and the GUI will relieve a lot of the work.
#TODO 3. Create new input flow. have integrated startup functionality to generate keys and files automatically.
#TODO 4. In the load_key block, if we blindly generate a new key while having an existing passwords file lingering, we
# won't be able to decrypt. May need to give a warning and if approved, generate new key and create new blank file?


def generate_key():
    global key_file
    key = Fernet.generate_key()
    with open(key_file, "wb") as file:
        file.write(key)


def load_key():
    try:
        read_key = open(key_file, "rb").read()
    except FileNotFoundError:
        print("Key file not found, generating new")
        # may need to have a check to see if passwords are already in file, will be using a different key,
        # will need to give a warning that we need to clean up the password file
        generate_key()
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

# Was used for initial password bulk creation, removing with introduction of gui
# def store_passwords(passwords, filename=password_file):
#     encrypted_passwords = {user: encrypt_password(pw) for user, pw in passwords.items()}
#     with open(filename, "w") as file:
#         json.dump({user: enc_pw.decode() for user, enc_pw in encrypted_passwords.items()}, file)


def check_passwords():
    try:
        with open(password_file, "r") as file:
            encrypted_passwords = json.load(file)
    except FileNotFoundError:
        print("Password file not found, creating blank")
        encrypted_passwords = {}
        with open(password_file, "w") as file:
            json.dump(encrypted_passwords, file)
        return encrypted_passwords
    else:
        return {user: decrypt_password(enc_pw.encode()) for user, enc_pw in encrypted_passwords.items()}


def get_password(requested_user, password_json_file):
    with open(password_json_file, "r") as file:
        encrypted_passwords = json.load(file)
    if requested_user in encrypted_passwords:
        return decrypt_password(encrypted_passwords[requested_user].encode())
    else:
        return None


def update_password(user, password, password_json_file):
    with open(password_json_file, "r") as file:
        encrypted_passwords = json.load(file)
    encrypted_password = encrypt_password(password).decode()
    encrypted_passwords[user] = encrypted_password
    with open(password_json_file, "w") as file:
        json.dump(encrypted_passwords, file)
    print(f"Password for {user} has been updated/added.")


def copy_passwords_to_clipboard(password_to_copy):
    pyperclip.copy(password_to_copy)


def pull_password_from_clipboard():
    return pyperclip.paste()


def display_users(filename=password_file):
    with open(filename, "r") as file:
        users = json.load(file).keys()
        return [user_id for user_id in users]


# load_key()

# if __name__ == "__main__":
    # operation = sys.argv[1].lower()
#     if len(sys.argv) == 4:
#         password=sys.argv[3]
#
#     if operation == "start":
#         answer=input("Start operation should only be done once, it will generate your secret key for encryption and decryption and create your initial json password file based on the initial_passwords dictionary. Are you sure? Y/N ").lower()
#         if answer == "y":
#             generate_key()
#             store_passwords(initial_passwords)
#         else:
#             print("Okay, exiting")
#             exit(0)
#     elif len(sys.argv) < 3:
#         print("Usage: get/put user <password>")
#         exit(1)
#     elif operation not in ("get", "put"):
#         print(f"Argument {operation} not valid, expecting 'get' / 'put'")
#         exit(1)
#     elif operation == "get":
#         user = sys.argv[2].lower()
#         if user not in check_passwords():
#             print(f"User Name {user} not found in password list, ensure password is loaded.")
#             print(f"Loaded Users: {[key for key in check_passwords()]}.")
#             exit(1)
#         else:
#             print(f"Password for {user} is {get_password(user)}, password is in your copy buffer.")
#             copy_passwords_to_clipboard(get_password(user))
test_user = "test_user1"
test_password = "test_passwor6"

print(get_password(test_user, password_file))
#     elif operation == "put":
#         user = sys.argv[2].lower()
#         if len(sys.argv) != 4:
#             print(f"Usage for put operation: <put> <user> <password>")
#         elif user in check_passwords():
#             if password == "clipboard":
#                 print(f"User name {user} found in passwords dictionary, will be updating with {pull_password_from_clipboard()} from the clipboard.")
#                 update_password(user, pull_password_from_clipboard())
#             else:
#                 print(f"User name {user} found in passwords dictionary, will be updating with {password}.")
#                 update_password(user, password)
#         else:
#             if password == "clipboard":
#                 print(f"Adding {user}'s password {pull_password_from_clipboard()} from the clipboard.")
#                 update_password(user, pull_password_from_clipboard())
#             else:
#                 print(f"Adding user name {user} password {password}.")
#                 update_password(user, password)