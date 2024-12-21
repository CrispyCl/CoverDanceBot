import datetime
from logging import Logger

from sqlalchemy.exc import IntegrityError, NoResultFound

from models import Cover, DifficultEnum
from repository import CoverDataClass, DefaultCoverRepository, GenderEnum
from service import DefaultCoverService


class CoverService(DefaultCoverService):
    """Cover Service class"""

    def __init__(self, repository: DefaultCoverRepository, logger: Logger):
        self.repo = repository
        self.log = logger

    async def create(self, cover_data: CoverDataClass) -> int:
        try:
            return await self.repo.create(cover_data)
        except IntegrityError as e:
            self.log.warning("CoverRepository: %s" % e)
        except Exception as e:
            self.log.error("CoverRepository: %s" % e)
        return 0

    async def get_one(self, id: int) -> Cover:
        try:
            return await self.repo.get_one(id)
        except Exception as e:
            self.log.error("CoverRepository: %s" % e)
        return None

    async def get(self) -> list[Cover]:
        try:
            return await self.repo.get()
        except Exception as e:
            self.log.error("CoverRepository: %s" % e)
        return []

    async def find(
        self,
        gender: str,
        members: int,
        difficult: str,
        start_year: int,
        end_year: int,
    ) -> list[Cover]:
        try:
            return await self.repo.find(
                GenderEnum(gender),
                members,
                DifficultEnum(difficult),
                datetime.date(start_year, 1, 1),
                datetime.date(end_year, 12, 31),
            )
        except Exception as e:
            self.log.error("CoverRepository: %s" % e)
        return []

    async def update(self, id: int, cover_data: CoverDataClass) -> Cover:
        try:
            return await self.repo.update(id, cover_data)
        except NoResultFound as e:
            self.log.warning("CoverRepository: %s" % e)
        except Exception as e:
            self.log.error("CoverRepository: %s" % e)
        return None

    async def delete(self, id: int) -> bool:
        try:
            return await self.repo.delete(id)
        except NoResultFound as e:
            self.log.warning("CoverRepository: %s" % e)
        except Exception as e:
            self.log.error("CoverRepository: %s" % e)
        return False


__all__ = ["CoverService"]
