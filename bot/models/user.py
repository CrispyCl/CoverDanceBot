from datetime import date, datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Integer

from database import Base


class LanguageEnum(PyEnum):
    EN = "en"
    RU = "ru"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    token_count = Column(Integer, default=0)
    token_last_receipt = Column(Date, default=date.today())
    language = Column(Enum(LanguageEnum), default=LanguageEnum.EN)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return (
            f"<User(id={self.id}, language={self.language}, token_count={self.token_count}, is_staff={self.is_staff})>"
        )


__all__ = ["User", "LanguageEnum"]
