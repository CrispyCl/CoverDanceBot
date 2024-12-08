from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from filters import IsAdminFilter

router = Router()
router.message.filter(~IsAdminFilter())


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command

    Args:
        message (Message):
    """
    button1 = KeyboardButton(text=_("Find a practical video"))
    button2 = KeyboardButton(text=_("Balance"))
    reply_kb = ReplyKeyboardMarkup(keyboard=[[button1, button2]], resize_keyboard=True)
    await message.answer(
        _(
            "Hi, this is a bot for finding practice videos by (what we have...).\n\nSelect Video Search "
            "to get started, or press /help to see a description of all available actions.",
        ),
        reply_markup=reply_kb,
    )


@router.message(Command(commands="help"))
async def process_help_command(message: Message) -> None:
    await message.answer(_("This is the user help section"))


__all__ = ["router"]
