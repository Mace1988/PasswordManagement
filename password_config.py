"""
The key_file and password_file are files that will be generated during the initial start and the utility will need read/write access to. The passwords are encrypted with the key.
"""

key_file = r"\Users\franc\Documents\Projects\PasswordManagement\secret.key"
password_file = r"\Users\franc\Documents\Projects\PasswordManagement\passwords.json"

"""
The initial passwords dictionary is used for an initial bulk load of passwords. It should not be used for ongoing additions.

"""
initial_passwords = {
    "d_aa-a673538": "8=LQbWVLAYvtqu/d",
    "q_aa-a673538": "jsAb!JUmO2/IyCae",
    "aa-a673538": "h6Lru/epx85i2j0x"
}