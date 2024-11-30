import asyncio
from contextlib import suppress
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import Redis, RedisStorage

from config import Config, load_config
from database import PostgresDatabase
from handlers import user_router
from logger import get_logger


async def shutdown(bot: Bot, dp: Dispatcher, logger: logging.Logger) -> None:
    """
    Gracefully shutdown bot and resources.
    """

    logger.info("Shutting down bot...")

    logger.debug("Closing storage...")
    await dp.fsm.storage.close()

    logger.debug("Closing bot...")
    await bot.session.close()

    logger.info("Bot shut down successfully.")


async def main() -> None:
    # Loading the config
    config: Config = load_config()

    # Configuring the logging
    logger = get_logger("main", config.logger)
    logger.info("Starting bot...")

    logger.debug("Initialising the storage object...")
    redis = Redis(host=config.redis.host, port=config.redis.port, db=config.redis.db)
    storage = RedisStorage(redis=redis)

    logger.debug("Connecting to the database...")
    db = PostgresDatabase(config=config.posgres)
    try:
        await db.init_db()
    except Exception as e:
        logger.fatal("Database connection failed: %s", str(e))
        return

    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    logger.debug("Registering routers...")
    dp.include_router(user_router)

    # Graceful shutdown handling
    logger.info("Bot was started")
    try:
        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)
    except Exception as e:
        logger.error("An error occurred: %s", e)
    finally:
        await shutdown(bot, dp, logger)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())


__all__ = []
