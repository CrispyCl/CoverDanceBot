from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


class ChooseGenderToSearchKeyboard:
    def __call__(self) -> ReplyKeyboardMarkup:
        buttons: list[list[KeyboardButton]] = [
            [
                KeyboardButton(text=_("Male")),
                KeyboardButton(text=_("No matter")),
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


class CoverViewKeyboard:
    def __call__(self):
        buttons: list[list[KeyboardButton]] = [
            [
                KeyboardButton(text=_("🔍Find more videos")),
                KeyboardButton(text=_("🔙Back to menu")),
            ],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


__all__ = ["ChooseGenderToSearchKeyboard", "ChooseDifficultKeyboard", "CoverViewKeyboard"]
