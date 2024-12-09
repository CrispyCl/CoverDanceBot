from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from database import DefaultDatabase
from models import Cover, DifficultEnum
from repository import CoverDataClass, DefaultCoverRepository, GenderEnum


class CoverRepository(DefaultCoverRepository):
    """Cover Repository class"""

    def __init__(self, database: DefaultDatabase):
        self.db = database

    async def create(self, cover_data: CoverDataClass) -> int:
        async with self.db.get_session() as session:
            session: AsyncSession
            if cover_data.members > 10:
                cover_data.members = 10
            cover = Cover(
                author_id=cover_data.author_id,
                name=cover_data.name,
                url=cover_data.url,
                gender=cover_data.gender,
                members=cover_data.members,
                difficult=cover_data.difficult,
                publish_date=cover_data.publish_date,
            )
            session.add(cover)
            try:
                await session.commit()
                return cover.id

            except IntegrityError as e:
                await session.rollback()
                raise IntegrityError(
                    statement=e.statement,
                    params=e.params,
                    orig=f"User with id={cover_data.author_id} does not exist",
                )

            except Exception as e:
                await session.rollback()
                raise e

    async def get_one(self, id: int) -> Cover:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                return await session.get(Cover, id)
            except Exception as e:
                raise e

    async def get(self) -> list[Cover]:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                return (await session.execute(select(Cover).order_by(Cover.id))).scalars().all()
            except Exception as e:
                raise e

    async def find(
        self,
        gender: GenderEnum,
        members: int,
        difficult: DifficultEnum,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[Cover]:
        async with self.db.get_session() as session:
            session: AsyncSession
            query = (
                select(Cover)
                .order_by(Cover.id)
                .where(
                    Cover.members == members,
                    Cover.difficult == difficult,
                    Cover.publish_date.between(start_date, end_date),
                )
            )
            if gender != GenderEnum.NOT_STATED:
                query = query.where(Cover.gender == gender.value)
            try:
                return (await session.execute(query)).scalars().all()
            except Exception as e:
                raise e

    async def update(self, id: int, cover_data: CoverDataClass) -> Cover:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                cover = await session.get(Cover, id)
                if not cover:
                    raise NoResultFound(f"Cover with id={id} does not exist")
                if cover_data.members > 10:
                    cover_data.members = 10

                cover.gender = cover_data.gender
                if cover_data.name:
                    cover.name = cover_data.name
                if cover_data.url:
                    cover.url = cover_data.url
                if cover_data.members:
                    cover.members = cover_data.members
                if cover_data.difficult:
                    cover.difficult = cover_data.difficult
                await session.commit()
                return cover

            except Exception as e:
                await session.rollback()
                raise e

    async def delete(self, id: int) -> bool:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                cover = await session.get(Cover, id)
                if not cover:
                    raise NoResultFound(f"Cover with id={id} does not exist")
                await session.delete(cover)
                await session.commit()
                return True

            except Exception as e:
                raise e


__all__ = ["CoverRepository"]
