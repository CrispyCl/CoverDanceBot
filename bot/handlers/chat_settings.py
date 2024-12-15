from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _, I18n


from keyboards import BaseAdminKeyboard, BaseSuperadminKeyboard, LanguageSelectionInlineKeyboard, MainUserKeyboard
from service import DefaultUserService


router = Router()


@router.message(lambda m: m.text == _("🈹Change language"))
async def change_user_language(message: Message):
    await message.delete()
    await message.answer(text=_("Choose the neccesary language"), reply_markup=LanguageSelectionInlineKeyboard()())


@router.callback_query(F.data == "change_language_to_russian")
async def change_language_to_russian(callback: CallbackQuery, i18n: I18n, user_service: DefaultUserService):
    await callback.message.delete()
    await user_service.update_language(callback.from_user.id, "ru")
    i18n.ctx_locale.set("ru")
    user = await user_service.get_one(callback.from_user.id)
    if user.is_superuser:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=BaseSuperadminKeyboard()(),
        )
    elif user.is_staff:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=BaseAdminKeyboard()(),
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
    user = await user_service.get_one(callback.from_user.id)
    if user.is_superuser:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=BaseSuperadminKeyboard()(),
        )
    elif user.is_staff:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=BaseAdminKeyboard()(),
        )
    else:
        await callback.message.answer(
            text=_("Your language has been changed to English"),
            reply_markup=MainUserKeyboard()(),
        )


__all__ = ["router"]
