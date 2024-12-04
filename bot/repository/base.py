from abc import ABC, abstractmethod
from dataclasses import dataclass

from database import DefaultDatabase
from models import User


@dataclass
class UserDataClass:
    id: int
    token_count: int = 2_000
    is_staff: bool = False


class DefaultUserRepository(ABC):
    """Abstract UserRepository class"""

    @abstractmethod
    def __init__(self, database: DefaultDatabase):
        self.db = database

    @abstractmethod
    async def create(self, user_data: UserDataClass) -> int:
        """Create user method."""

    @abstractmethod
    async def get(self, id: int) -> User:
        """Get user method."""

    @abstractmethod
    async def list(self) -> list[User]:
        """List users method."""

    @abstractmethod
    async def update_token(self, id: int, difference: int) -> User:
        """Update user token method."""

    @abstractmethod
    async def update_role(self, id: int, is_staff: bool) -> User:
        """Update user role method."""


__all__ = ["DefaultUserRepository", "UserDataClass"]
