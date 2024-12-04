from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from config import load_config
from database import Base
from models import User  # noqa: F401

db_config = load_config()
database_url = db_config.posgres.get_database_url()

config = context.config
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

fileConfig(config.config_file_name)


def run_migrations_online():
    connectable = create_engine(
        database_url.replace("postgresql+asyncpg", "postgresql"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()


__all__ = []
