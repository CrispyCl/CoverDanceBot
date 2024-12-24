from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


class MainUserKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [KeyboardButton(text=_("🔍Find practice video"))],
            [KeyboardButton(text=_("💰Balance")), KeyboardButton(text=_("✨Daily bonus"))],
            [KeyboardButton(text=_("🈹Change language"))],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


class LanguageSelectionInlineKeyboard:
    def __call__(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="English", callback_data="change_language_to_english")],
                [InlineKeyboardButton(text="Русский", callback_data="change_language_to_russian")],
            ],
        )


__all__ = ["MainUserKeyboard", "LanguageSelectionInlineKeyboard"]
