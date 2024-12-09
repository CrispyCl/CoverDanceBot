from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from filters.has_permissions import IsAdminFilter, IsSuperAdminFilter


router = Router()
router.message.filter(IsAdminFilter())


@router.message(CommandStart(), IsSuperAdminFilter())
async def proccess_super_admin_start(message: Message) -> None:
    button1 = KeyboardButton(text=_("Add admin"))
    button2 = KeyboardButton(text=_("Add video"))
    reply_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1, button2]], resize_keyboard=True)
    await message.answer(
        _(
            "Welcome to the CoverDanceBot control menu.\n\nClick add admin to add a user who can make"
            "changes to the database.\n\nPress /help in the menu to see a description of all the actions"
            "available to you.",
        ),
        reply_markup=reply_kb,
    )


@router.message(Command(commands="help"), IsSuperAdminFilter())
async def process_super_admin_help_button(message: Message) -> None:
    await message.answer(_("This is the /help menu"))


__all__ = ["router"]
