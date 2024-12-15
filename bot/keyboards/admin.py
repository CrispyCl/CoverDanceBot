from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


class BaseSuperadminKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [KeyboardButton(text=_("🔍Find practice video"))],
            [
                KeyboardButton(text=_("⚙️Admin management")),
                KeyboardButton(text=_("📽️Add video")),
            ],
            [KeyboardButton(text=_("🈹Change language"))],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


class BaseAdminKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [KeyboardButton(text=_("🔍Find practice video"))],
            [KeyboardButton(text=_("📽️Add video"))],
            [KeyboardButton(text=_("🈹Change language"))],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


class AdminManagementInlineKeyboard:
    def __call__(self) -> InlineKeyboardMarkup:
        buttons: list[list[InlineKeyboardButton]] = [
            [
                InlineKeyboardButton(text=_("➕Add admin"), callback_data="add_admin_button_pressed"),
                InlineKeyboardButton(text=_("❌Delete admin"), callback_data="delete_admin_button_pressed"),
            ],
            [InlineKeyboardButton(text=_("🔙Back"), callback_data="back_button_pressed")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)


class ChooseGenderKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [
                KeyboardButton(text=_("Male")),
                KeyboardButton(text=_("Female")),
            ],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


class ChooseDifficultKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [
                KeyboardButton(text=_("Easy")),
                KeyboardButton(text=_("Middle")),
                KeyboardButton(text=_("Hard")),
            ],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


class SaveCoverKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [KeyboardButton(text=_("✅Save cover"))],
            [KeyboardButton(text=_("🔄️Redo the cover form"))],
            [KeyboardButton(text=_("❌Don't save the cover"))],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


class BackButton:
    def __call__(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=_("🔙Back"), callback_data="back_button_pressed")]],
        )


__all__ = [
    "BaseSuperadminKeyboard",
    "BackButton",
    "BaseAdminKeyboard",
    "AdminManagementInlineKeyboard",
    "ChooseGenderKeyboard",
    "ChooseDifficultKeyboard",
    "SaveCoverKeyboard",
]
