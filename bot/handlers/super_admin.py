from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _


from filters import IsSuperAdminFilter
from keyboards import AdminManagementInlineKeyboard, BackButton, BaseSuperadminKeyboard
from service import DefaultUserService


router = Router()
router.message.filter(IsSuperAdminFilter())


class FSMSuperAdmin(StatesGroup):
    main_menu = State()
    admin_management_menu = State()
    fill_username = State()


@router.message(CommandStart(), IsSuperAdminFilter())
async def proccess_super_admin_start(message: Message, state: FSMContext) -> None:
    await message.delete()
    await message.answer(
        _(
            "Welcome to the CoverDanceBot admin panel.\n\nClick add admin to add a user who can make"
            "changes to the database.\n\nPress /help in the menu to see a description of all the actions"
            "available to you.",
        ),
        reply_markup=BaseSuperadminKeyboard()(),
    )
    await state.set_state(FSMSuperAdmin.main_menu)


@router.message(Command(commands="help"), IsSuperAdminFilter())
async def process_super_admin_help_button(message: Message) -> None:
    await message.answer(_("This is the /help menu"))


@router.message(lambda m: m.text == _("⚙️Admin management"), StateFilter(FSMSuperAdmin.main_menu))
async def admin_management_menu(message: Message, user_service: DefaultUserService, state: FSMContext) -> None:
    await message.delete()
    await message.answer(
        text=_("Admins: \n") + "\n".join([str(user.id) for user in await user_service.get() if user.is_staff]),
        reply_markup=AdminManagementInlineKeyboard()(),
    )
    await state.set_state(FSMSuperAdmin.admin_management_menu)


@router.callback_query(F.data == "add_admin_button_pressed", StateFilter(FSMSuperAdmin.admin_management_menu))
async def ask_for_new_admin_name(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text=_("Pleace enter the user id"))
    await callback.message.edit_reply_markup(reply_markup=BackButton()())
    await state.set_state(FSMSuperAdmin.fill_username)


@router.callback_query(F.data == "delete_admin_button_pressed", StateFilter(FSMSuperAdmin.admin_management_menu))
async def ask_for_delete_admin_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=_("Pleace enter the user id"))
    await state.set_state(FSMSuperAdmin.fill_username)


@router.callback_query(F.data == "back_button_pressed", StateFilter(FSMSuperAdmin.admin_management_menu))
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(FSMSuperAdmin.main_menu)


@router.callback_query(F.data == "back_button_pressed", StateFilter(FSMSuperAdmin.fill_username))
async def back_to_admin_management_menu(callback: CallbackQuery, state: FSMContext, user_service: DefaultUserService):
    await callback.message.edit_text(
        text=_("Admins: \n") + "\n".join([str(user.id) for user in await user_service.get() if user.is_staff]),
    )
    await callback.message.edit_reply_markup(reply_markup=AdminManagementInlineKeyboard()())
    await state.set_state(FSMSuperAdmin.admin_management_menu)


@router.message(F.text, StateFilter(FSMSuperAdmin.fill_username))
async def add_new_admin(message: Message, state: FSMContext, user_service: DefaultUserService) -> None:
    await message.delete()
    if message.text.isdigit():
        id = int(message.text)
        user = await user_service.get_or_create(id, message.from_user.username)
        if not user:
            await message.answer(_("Pleace enter correct user id"))
        elif user.is_staff:
            await message.answer(text=_("This user is already an admin, try again or press back"))
            await state.set_state(FSMSuperAdmin.admin_management_menu)
        else:
            await user_service.update_role(user.id, True)
            await message.answer(text=_("Admin successfully added"))
            await state.set_state(FSMSuperAdmin.admin_management_menu)

    else:
        await message.answer(_("Pleace enter correct user id"))


__all__ = ["router"]
