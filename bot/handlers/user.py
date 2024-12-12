from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _, I18n

from keyboards import BaseSuperadminKeyboard, LanguageSelectionInlineKeyboard, MainUserKeyboard
from models import User
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


@router.message(lambda m: m.text == _("💰Balance"), StateFilter(FSMUser.main_menu))
async def show_balance(message: Message, current_user: User, user_service: DefaultUserService):
    await message.delete()
    await message.answer(
        _(
            "Your balance: {token_count}\n\n"
            "The cost of video retrieval is 500 tokens\n\n"
            "To top up your token balance, take advantage of the daily bonus",
        ).format(
            token_count=current_user.token_count,
        ),
    )


@router.message(lambda m: m.text == _("✨Daily bonus"), StateFilter(FSMUser.main_menu))
async def process_daily_bonus_reciept(message: Message, current_user: User, user_service: DefaultUserService):
    is_token_updated = await user_service.update_token(current_user.id, 2000, True)
    current_user = await user_service.get(current_user.id)
    await message.delete()

    if is_token_updated:
        await message.answer(
            _(
                "You received a daily bonus\n\nYour current balance: {token_count}",
            ).format(
                token_count=current_user.token_count,
            ),
        )
    else:
        await message.answer(
            _(
                "You've already received a bonus today\n\n" "Please come back tomorrow",
            ),
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
    user = await user_service.get(callback.from_user.id)
    if user.is_staff:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=BaseSuperadminKeyboard()(),
        )
    else:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=MainUserKeyboard()(),
        )


@router.callback_query(F.data == "change_language_to_english")
async def change_language_to_english(callback: CallbackQuery, i18n: I18n, user_service: DefaultUserService):
    await callback.message.delete()
    await user_service.update_language(callback.from_user.id, "en")
    i18n.ctx_locale.set("en")
    user = await user_service.get(callback.from_user.id)
    if user.is_staff:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=BaseSuperadminKeyboard()(),
        )
    else:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=MainUserKeyboard()(),
        )


__all__ = ["router"]
