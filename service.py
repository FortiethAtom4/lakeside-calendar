
import scrypt
import secrets

import db
from models import User, Reservation


def new_user(email: str, pw: str, first_name: str, last_name: str) -> bool:
    salt: bytes = secrets.token_bytes(32)

    encrypted_pw: bytes = scrypt.hash(pw,salt)

    return db.insert_user(email,encrypted_pw,salt,first_name,last_name)

def login(email: str, pw: str) -> User | None:
    the_user = db.get_user_by_email(email)

    if the_user == None:
        print("Not found")
        return None

    try_pass = scrypt.hash(pw,the_user.password_salt)

    if try_pass == the_user.password:
        print("logged in")
        return the_user

    print("wrong pw")
    return None

def get_user(id: int):
    return db.load_user(id)
    


    
    