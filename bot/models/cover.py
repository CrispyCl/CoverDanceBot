from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, orm, String

from database import Base


class DifficultEnum(PyEnum):
    EASY = "easy"
    MIDDLE = "middle"
    HARD = "hard"


class Cover(Base):
    __tablename__ = "covers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    gender = Column(Boolean, nullable=False)
    members = Column(Integer, nullable=False)
    difficult = Column(Enum(DifficultEnum), nullable=False)
    publish_date = Column(Date, nullable=False)

    def __repr__(self):
        return (
            f"Cover(id={self.id}, "
            f"name='{self.name}', "
            f"url='{self.url}', "
            f"gender={self.gender}, "
            f"members={self.members}, "
            f"difficult={self.difficult.value}, "
            f"publish_date={self.publish_date})"
        )

    author = orm.relationship("User", back_populates="covers", lazy="joined")


__all__ = ["Cover", "DifficultEnum"]
