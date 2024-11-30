from contextlib import asynccontextmanager
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database import Base, DefaultDatabase


@dataclass
class PostgresConfig:
    user: str
    password: str
    db_name: str
    host: str
    port: int


class Database(DefaultDatabase):
    """Posgres Database class"""

    def __init__(self, config: PostgresConfig):
        self.config = config
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}:{config.port}/{config.db_name}",
            echo=False,
        )
        self.async_session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def init_db(self):
        """Creating all tables in the database."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db(self):
        """Deleting all tables from the database."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def get_session(self):
        """Context manager for sessions."""
        async with self.async_session() as session:
            yield session


__all__ = ["Database", "PostgresConfig"]
