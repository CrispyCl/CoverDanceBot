from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command

    Args:
        message (Message):
    """

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


__all__ = ["router"]
