from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot


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
        tg_bot=TgBot(token=env("BOT_TOKEN")),
    )


__all__ = ["Config", "load_config"]
