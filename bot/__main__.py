import asyncio
from contextlib import suppress
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.utils.i18n import I18n

from config import Config, load_config
from database import DefaultDatabase, PostgresDatabase
from handlers import admin_router, chat_settings_router, user_router
from keyboards.set_menu import setup_menu
from logger import get_logger
from middleware import setup as setup_middlewares
from repository import CoverRepository, UserRepository
from service import CoverService, UserService


async def shutdown(bot: Bot, dp: Dispatcher, logger: logging.Logger, redis: Redis | None, db: DefaultDatabase) -> None:
    """
    Gracefully shutdown bot and resources.
    """

    logger.info("Shutting down bot...")

    logger.debug("Closing storage...")
    await dp.fsm.storage.close()
    if redis:
        try:
            await redis.aclose()
        except Exception as e:
            logger.error("Failed to close Redis storage: %s", str(e))

    logger.debug("Stopping bot...")
    try:
        await bot.session.close()
    except Exception as e:
        logger.error("Failed to close bot session: %s", str(e))

    logger.debug("Closing database connection...")
    try:
        await db.close()
    except Exception as e:
        logger.error("Failed to close database connection: %s", str(e))

    logger.info("Bot shut down successfully.")


async def main() -> None:
    # Loading the config
    config: Config = load_config()

    # Configuring the logging
    logger = get_logger("main", config.logger)
    logger.info("Starting bot...")

    logger.debug("Initialising the storage object...")
    redis = Redis(host=config.redis.host, port=config.redis.port, db=config.redis.db)
    try:
        await redis.ping()
    except Exception as e:
        logger.fatal("Storage initialisation failed: %s", str(e))
        return
    storage = RedisStorage(redis=redis)

    logger.debug("Connecting to the database...")
    db = PostgresDatabase(config=config.postgres)
    try:
        await db.init_db()
    except Exception as e:
        logger.fatal("Database connection failed: %s", str(e))
        return

    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    dp.workflow_data["logger"] = logger

    logger.debug("Loading menu...")
    try:
        await setup_menu(bot)
    except Exception as e:
        logger.fatal("Menu loading failed: %s", str(e))

    logger.debug("Registering repositories...")
    user_repository = UserRepository(db)
    cover_repository = CoverRepository(db)

    logger.debug("Registering services...")
    user_service = UserService(user_repository, logger)
    dp.workflow_data["user_service"] = user_service
    cover_service = CoverService(cover_repository, logger)
    dp.workflow_data["cover_service"] = cover_service

    logger.debug("Registering routers...")
    dp.include_router(chat_settings_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    logger.debug("Initialising i18n...")
    try:
        i18n = I18n(path="locales", default_locale="en", domain="messages")
    except Exception as e:
        logger.fatal("Initialising failed: %s", str(e))
        return

    logger.debug("Registering middlewares...")
    setup_middlewares(dp, logger, user_service, i18n)

    # Graceful shutdown handling
    try:
        logger.debug("Deleting webhook...")
        await bot.delete_webhook(drop_pending_updates=True)

        logger.info("Bot was started")
        await dp.start_polling(bot)
    except Exception as e:
        logger.fatal("An error occurred: %s", e)
    finally:
        await shutdown(bot, dp, logger, redis, db)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())


__all__ = []
