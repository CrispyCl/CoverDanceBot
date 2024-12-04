from abc import ABC, abstractmethod
from logging import Logger

from models import User
from repository.user import DefaultUserRepository


class DefaultUserService(ABC):
    """Abstract UserService class"""

    @abstractmethod
    def __init__(self, repository: DefaultUserRepository, logger: Logger):
        self.repo = repository
        self.log = logger

    @abstractmethod
    async def create(self, id: int, is_staff: bool = False, token_count: int = 2_000) -> int:
        """Create user method."""

    @abstractmethod
    async def get(self, id: int) -> User:
        """Get user method."""

    @abstractmethod
    async def get_or_create(self, id: int) -> User:
        """Get or create user method."""

    @abstractmethod
    async def list(self) -> list[User]:
        """List users method."""

    @abstractmethod
    async def update_token(self, id: int, difference: int, is_daily: bool = False) -> User:
        """Update user tocker method."""

    @abstractmethod
    async def update_role(self, id: int, is_staff: bool) -> User:
        """Update user role method."""

    @abstractmethod
    async def is_admin(self, id: int) -> bool:
        """Is admin check method."""

    @abstractmethod
    async def is_super_admin(self, id: int) -> bool:
        """Is super admin check method."""


__all__ = ["DefaultUserService"]
