from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


class BaseSuperadminKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [KeyboardButton(text=_("Admin management")), KeyboardButton(text=_("Add video"))],
            [KeyboardButton(text=_("🈹Change language"))],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


class AdminManagementInlineKeyboard:
    def __call__(self) -> InlineKeyboardMarkup:
        buttons: list[list[InlineKeyboardButton]] = [
            [
                InlineKeyboardButton(text=_("Add admin"), callback_data="add_admin_button_pressed"),
                InlineKeyboardButton(text=_("Delete admin"), callback_data="delete_admin_button_pressed"),
            ],
            [InlineKeyboardButton(text=_("Back"), callback_data="back_button_pressed")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)


class BackButton:
    def __call__(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=_("Back"), callback_data="back_button_pressed")]],
        )


__all__ = ["BaseSuperadminKeyboard", "BackButton"]
