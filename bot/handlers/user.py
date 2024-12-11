from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _, I18n

from keyboards import LanguageSelectionInlineKeyboard, MainUserKeyboard
from service import DefaultUserService


router = Router()


class FSMUser(StatesGroup):
    main_menu = State()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext) -> None:
    """This handler receives messages with `/start` command

    Args:
        message (Message):
    """

    await message.answer(
        text=_(
            "Hi, this is a bot for finding practice videos by (what we have...).\n\n"
            "Select Video Search to get started, or press /help to see a description "
            "of all available actions.",
        ),
        reply_markup=MainUserKeyboard()(),
    )
    await state.set_state(FSMUser.main_menu)


@router.message(Command(commands="help"))
async def process_help_command(message: Message) -> None:
    await message.delete()
    await message.answer(
        text=_(
            "<b>User assistance menu</b>\n\n"
            "<b>/start</b> "
            "- Start bot or update language settings\n\n"
            "<b>[Find practice videos]</b> "
            "- search for practice videos based on year, gender and dance direction\n\n"
            "<b>[Balance]</b> "
            "- go to the balance menu\n\n"
            "<b>[Daily Bonus]</b> "
            "- Receive a daily bonus in the form of tokens for balance\n\n"
            "<b>[Change Language]</b>"
            "- Change the language of the bot interface.\n\n",
        ),
        parse_mode="HTML",
    )


@router.message(lambda m: m.text == _("🈹Change language"))
async def change_user_language(message: Message):
    await message.delete()
    await message.answer(text=_("Choose the neccesary language"), reply_markup=LanguageSelectionInlineKeyboard()())


@router.callback_query(F.data == "change_language_to_russian")
async def change_language_to_russian(callback: CallbackQuery, i18n: I18n, user_service: DefaultUserService):
    await callback.message.delete()
    await user_service.update_language(callback.from_user.id, "ru")
    i18n.ctx_locale.set("ru")
    await callback.message.answer(text=_("Your language has been changed"), reply_markup=MainUserKeyboard()())


@router.callback_query(F.data == "change_language_to_english")
async def change_language_to_english(callback: CallbackQuery, i18n: I18n, user_service: DefaultUserService):
    await callback.message.delete()
    await user_service.update_language(callback.from_user.id, "en")
    i18n.ctx_locale.set("en")
    await callback.message.answer(text=_("Your language has been changed"), reply_markup=MainUserKeyboard()())


__all__ = ["router"]
