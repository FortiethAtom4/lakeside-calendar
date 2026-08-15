from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import User, Base, Reservation

engine = create_engine("sqlite:///lakeside.db")

Base.metadata.create_all(engine)

def insert_user(email: str, pw_hash: bytes, pw_salt: bytes, first_name: str = "", last_name: str = "") -> bool:
    with Session(engine) as session:
        new_user = User(
            email=email,
            password=pw_hash,
            password_salt = pw_salt,
            first_name=first_name,
            last_name=last_name)
        query = select(User).where(User.email == email)
        user_exists = session.scalar(query)

        if user_exists == None:
            session.add(new_user)
            session.commit()
            return True

        return False

def load_user(id: int) -> User | None:
    with Session(engine) as session:
        return session.scalar(select(User).where(User.user_id == id))

def get_user_by_email(email: str) -> User | None:
    with Session(engine) as session:
        return session.scalar(select(User).where(User.email == email))


