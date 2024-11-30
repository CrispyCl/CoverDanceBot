from dataclasses import dataclass

from environs import Env

from database import PostgresConfig
from logger import LoggerConfig


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int


@dataclass
class BotConfig:
    token: str
    debug: bool


@dataclass
class Config:
    bot: BotConfig
    logger: LoggerConfig
    redis: RedisConfig
    posgres: PostgresConfig


def load_config(path: str | None = None) -> Config:
    """Load config

    Args:
        path (str | None, optional): Path to your env file. Defaults to None.

    Returns:
        Config:
    """
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=BotConfig(token=env("BOT_TOKEN", default=""), debug=env.bool("DEBUG", default=True)),
        logger=LoggerConfig(debug=env.bool("DEBUG", default=True), file_path=env("LOGGER_FILE_PATH", default=None)),
        redis=RedisConfig(
            host=env("REDIS_HOST", default="localhost"),
            port=env.int("REDIS_PORT", default=6379),
            db=env.int("REDIS_DB", default=0),
        ),
        posgres=PostgresConfig(
            user=env("POSTGRES_USER", default=""),
            password=env("POSTGRES_PASSWORD", default=""),
            db_name=env("POSTGRES_DB", default=""),
            host=env("POSTGRES_HOST", default="localhost"),
            port=env.int("POSTGRES_PORT", default=5432),
        ),
    )


__all__ = ["Config", "load_config"]
