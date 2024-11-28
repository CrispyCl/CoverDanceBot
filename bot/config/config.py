from dataclasses import dataclass

from environs import Env

from logger.logger import LoggerConfig


@dataclass
class BotConfig:
    token: str
    debug: bool


@dataclass
class Config:
    bot: BotConfig
    logger: LoggerConfig


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
    )


__all__ = ["Config", "load_config"]
