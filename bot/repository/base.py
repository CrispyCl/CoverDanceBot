from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from enum import Enum

from database import DefaultDatabase
from models import Cover, DifficultEnum, LanguageEnum, User


@dataclass
class UserDataClass:
    id: int
    username: str
    token_count: int = 5_000
    is_staff: bool = False


@dataclass
class CoverDataClass:
    author_id: int
    name: str
    url: str
    gender: bool
    members: int
    difficult: DifficultEnum
    publish_date: datetime.date


class GenderEnum(Enum):
    MALE = True
    FEMALE = False
    NOT_STATED = None


class DefaultUserRepository(ABC):
    """Abstract UserRepository class"""

    @abstractmethod
    def __init__(self, database: DefaultDatabase):
        self.db = database

    @abstractmethod
    async def create(self, user_data: UserDataClass) -> int:
        """Create user method."""

    @abstractmethod
    async def get_one(self, id: int) -> User:
        """Get user by id method."""

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        """Get user by username method."""

    @abstractmethod
    async def get(self) -> list[User]:
        """Get users method."""

    @abstractmethod
    async def update_username(self, id: int, username: str) -> User:
        """Update user username method."""

    @abstractmethod
    async def update_token(self, id: int, difference: int) -> User:
        """Update user token method."""

    @abstractmethod
    async def update_role(self, id: int, is_staff: bool) -> User:
        """Update user role method."""

    @abstractmethod
    async def update_language(self, id: int, language: LanguageEnum) -> User:
        """Update user language method."""


class DefaultCoverRepository(ABC):
    """Abstract CoverRepository class"""

    @abstractmethod
    def __init__(self, database: DefaultDatabase):
        self.db = database

    @abstractmethod
    async def create(self, cover_data: CoverDataClass) -> int:
        """Create cover method."""

    @abstractmethod
    async def get_one(self, id: int) -> Cover:
        """Get cover method."""

    @abstractmethod
    async def get(self) -> list[Cover]:
        """List covers method."""

    @abstractmethod
    async def find(
        self,
        gender: GenderEnum,
        members: int,
        difficult: DifficultEnum,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[Cover]:
        """Find covers method."""

    @abstractmethod
    async def update(self, id: int, cover_data: CoverDataClass) -> Cover:
        """Update cover method."""

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete cover method."""


__all__ = ["DefaultCoverRepository", "DefaultUserRepository", "CoverDataClass", "UserDataClass"]
