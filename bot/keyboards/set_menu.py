from aiogram import Bot
from aiogram.types import BotCommand


async def setup_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="start", description="start"),
        BotCommand(command="help", description="help"),
    ]
    await bot.set_my_commands(main_menu_commands)


__all__ = ["setup_menu"]
