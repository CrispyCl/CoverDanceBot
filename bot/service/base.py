from abc import ABC, abstractmethod
from logging import Logger

from models import Cover, User
from repository import CoverDataClass, DefaultCoverRepository, DefaultUserRepository


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
    async def update_token(self, id: int, difference: int, is_daily: bool = False) -> bool:
        """Update user tocker method."""

    @abstractmethod
    async def update_role(self, id: int, is_staff: bool) -> bool:
        """Update user role method."""

    @abstractmethod
    async def update_language(self, id: int, language: str) -> bool:
        """Update user language method."""

    @abstractmethod
    async def is_admin(self, id: int) -> bool:
        """Is admin check method."""

    @abstractmethod
    async def is_super_admin(self, id: int) -> bool:
        """Is super admin check method."""


class DefaultCoverService(ABC):
    """Abstract CoverService class"""

    @abstractmethod
    def __init__(self, repository: DefaultCoverRepository, logger: Logger):
        self.repo = repository
        self.log = logger

    @abstractmethod
    async def create(self, cover_data: CoverDataClass) -> int:
        """Create cover method."""

    @abstractmethod
    async def get_one(self, id: int) -> Cover:
        """Get one cover method."""

    @abstractmethod
    async def get(self) -> list[Cover]:
        """Get covers method."""

    @abstractmethod
    async def find(
        self,
        gender: str,
        members: int,
        difficult: str,
        start_year: int,
        end_year: int,
    ) -> list[Cover]:
        """Find covers method"""

    @abstractmethod
    async def update(self, id: int, cover_data: CoverDataClass) -> Cover:
        """Update cover method."""

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete cover method."""


__all__ = ["DefaultCoverService", "DefaultUserService"]
