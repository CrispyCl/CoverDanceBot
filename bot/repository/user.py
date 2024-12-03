from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from database import DefaultDatabase
from exceptions import TokenDailyError, TokenNegativeError
from models import User
from repository import DefaultUserRepository, UserDataClass


class UserRepository(DefaultUserRepository):
    """User Repository class"""

    def __init__(self, database: DefaultDatabase):
        self.db = database

    async def create(self, user_data: UserDataClass) -> int:
        async with self.db.get_session() as session:
            session: AsyncSession
            if user_data.token_count > 10_000:
                user_data.token_count = 10_000
            elif user_data.token_count < 0:
                user_data.token_count = 0
            user = User(
                id=user_data.id,
                token_count=user_data.token_count,
                is_staff=user_data.is_staff,
            )
            session.add(user)
            try:
                await session.commit()
                return user.id

            except IntegrityError as e:
                await session.rollback()
                raise IntegrityError(
                    statement=e.statement,
                    params=e.params,
                    orig="UserRepository: User already exists",
                )

            except Exception as e:
                await session.rollback()
                raise e

    async def get(self, id: int) -> User:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                return await session.get(User, id), None
            except NoResultFound:
                return None, None
            except Exception as e:
                raise e

    async def list(self) -> list[User]:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                return (await session.execute(select(User).order_by(User.id))).scalars().all()
            except Exception as e:
                raise e

    async def update_token(self, id: int, difference: int, is_daily: bool = False) -> User:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                user = await session.get(User, id)
                if user is None:
                    raise NoResultFound(f"UserRepository: User with id={id} does not exist")

                user.token_count += difference
                if user.token_count > 10_000:
                    user.token_count = 10_000
                elif user.token_count < 0:
                    raise TokenNegativeError("UserRepository: Token count cannot be negative")
                if is_daily and difference > 0:
                    if user.token_last_receipt == datetime.now().date():
                        raise TokenDailyError("UserRepository: User has already received tokens today")
                    user.token_last_receipt = datetime.now()
                await session.commit()
                await session.refresh(user)
                return user

            except Exception as e:
                await session.rollback()
                raise e

    async def update_role(self, id: int, is_staff: bool) -> User:
        async with self.db.get_session() as session:
            session: AsyncSession
            try:
                user = await session.get(User, id)
                if user is None:
                    raise NoResultFound(f"UserRepository: User with id={id} does not exist")
                user.is_staff = is_staff
                await session.commit()
                await session.refresh(user)
                return user

            except Exception as e:
                await session.rollback()
                raise e


__all__ = ["UserRepository"]
