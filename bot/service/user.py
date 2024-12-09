from logging import Logger

from sqlalchemy.exc import IntegrityError, NoResultFound

from exceptions import TokenDailyError, TokenNegativeError
from models import LanguageEnum, User
from repository import UserDataClass, UserRepository
from service import DefaultUserService


class UserService(DefaultUserService):
    """User Service class"""

    def __init__(self, repository: UserRepository, logger: Logger):
        self.repo = repository
        self.log = logger

    async def create(self, id: int, is_staff: bool = False, token_count: int = 2_000) -> int:
        user = UserDataClass(id=id, token_count=token_count, is_staff=is_staff)
        try:
            return await self.repo.create(user_data=user)
        except IntegrityError as e:
            self.log.warning("UserRepository: %s" % e)
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return 0

    async def get(self, id: int) -> User:
        try:
            return await self.repo.get(id)
        except NoResultFound as e:
            self.log.warning("UserRepository: %s" % e)
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return None

    async def get_or_create(self, id: int) -> User:
        try:
            user = await self.repo.get(id)
            if not user:
                try:
                    id = await self.create(id)
                    return await self.repo.get(id)
                except IntegrityError as e:
                    self.log.warning("UserRepository: %s" % e)
                except Exception as e:
                    self.log.error("UserRepository: %s" % e)
                return None
            return user
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return None

    async def list(self) -> list[User]:
        try:
            return await self.repo.list()
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return []

    async def update_token(self, id: int, difference: int, is_daily: bool = False) -> bool:
        try:
            await self.repo.update_token(id, difference, is_daily)
            return True
        except (NoResultFound, TokenDailyError, TokenNegativeError) as e:
            self.log.warning("UserRepository: %s" % e)
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return False

    async def update_role(self, id: int, is_staff: bool) -> bool:
        try:
            await self.repo.update_role(id, is_staff)
            return True
        except NoResultFound as e:
            self.log.warning("UserRepository: %s" % e)
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return False

    async def update_language(self, id: int, language: str) -> bool:
        try:
            await self.repo.update_language(id, LanguageEnum(language))
            return True
        except (NoResultFound, ValueError) as e:
            self.log.warning("UserRepository: %s" % e)
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return False

    async def is_admin(self, id: int) -> bool:
        try:
            user = await self.repo.get(id)
            if not user:
                raise NoResultFound(f"User with id={id} does not exist")
            return user.is_staff
        except NoResultFound as e:
            self.log.warning("UserRepository: %s" % e)
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return False

    async def is_super_admin(self, id: int) -> bool:
        try:
            user = await self.repo.get(id)
            if not user:
                raise NoResultFound(f"User with id={id} does not exist")
            return user.is_superuser
        except NoResultFound as e:
            self.log.warning("UserRepository: %s" % e)
        except Exception as e:
            self.log.error("UserRepository: %s" % e)
        return False


__all__ = ["UserService"]
