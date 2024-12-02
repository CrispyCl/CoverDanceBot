from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    token_count = Column(Integer, default=0)
    token_last_receipt = Column(Date, default=date.today())
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.now())


__all__ = ["User"]
