from abc import ABC, abstractmethod

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DefaultDatabase(ABC):
    """Abstract Database class"""

    @abstractmethod
    async def init_db(self):
        """Creating all tables in the database."""

    @abstractmethod
    async def drop_db(self):
        """Deleting all tables from the database."""

    @abstractmethod
    async def get_session(self):
        """Context manager for sessions."""


__all__ = ["Base", "DefaultDatabase"]
