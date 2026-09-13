from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import LargeBinary
from typing import Optional
import datetime
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass

class User(UserMixin,Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[bytes] = mapped_column(LargeBinary)
    password_salt: Mapped[bytes] = mapped_column(LargeBinary)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    access_level: Mapped[Integer] = mapped_column(Integer)
    
    def get_id(self) -> str:
        return str(self.user_id)

class Reservation(Base):
    __tablename__ = "reservations"
    
    reservation_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    start_date: Mapped[datetime.date] = mapped_column(Date)
    end_date: Mapped[datetime.date] = mapped_column(Date)
    number_guests: Mapped[int] = mapped_column()
    others_allowed: Mapped[bool] = mapped_column()





