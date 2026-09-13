
import scrypt
import secrets

import calendar

import db
from models import User

import datetime as dt

ACCESS_LEVEL_MIN = 0 #can log in and that's about it
ACCESS_LEVEL_READ = 1 #can see reservations
ACCESS_LEVEL_WRITE = 2 #can make/edit reservations tied to the account
ACCESS_LEVEL_ADMIN = 3 #can manage/add/remove accounts and edit any reservation


WEEKDAYS: list[str] = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]




def new_user(email: str, pw: str, first_name: str, last_name: str, access_level: int) -> bool:
    if access_level < ACCESS_LEVEL_MIN or access_level > ACCESS_LEVEL_ADMIN:
        access_level = ACCESS_LEVEL_MIN

    salt: bytes = secrets.token_bytes(32)

    encrypted_pw: bytes = scrypt.hash(pw,salt)

    return db.insert_user(email,encrypted_pw,salt, access_level, first_name, last_name)

def login(email: str, pw: str) -> User | None:
    the_user = db.get_user_by_email(email)

    if the_user == None:
        return None

    try_pass = scrypt.hash(pw,the_user.password_salt)

    if try_pass == the_user.password:
        return the_user

    return None

def get_user(id: int):
    return db.load_user(id)

def prepare_calendar(this_year: int, this_month: int):
    global WEEKDAYS

    this_date: dt.datetime = dt.datetime(this_year,this_month,1)

    next_month: int = 1 if this_month == 12 else this_month + 1
    next_year: int = this_year + 1 if next_month == 1 else this_year

    previous_month: int = 12 if this_month == 1 else this_month - 1
    previous_year: int = this_year - 1 if this_month == 12 else this_year


    body_data = {
        "this_year":this_year,
        "next_year":next_year,
        "previous_year":previous_year,
        "this_month":this_month,
        "next_month":next_month,
        "previous_month":previous_month,
        "calendar":get_calendar(this_year,this_month),
        "month_name":this_date.strftime("%B"),
        "weekdays":WEEKDAYS
    }

    return body_data


def get_calendar(year: int, month: int) -> list[list[int]]:
    # weekdays start on Monday in each array
    return calendar.monthcalendar(year,month)







    
    