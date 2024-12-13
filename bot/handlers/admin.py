from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _


from filters import IsAdminFilter, IsSuperAdminFilter
from keyboards import AdminManagementInlineKeyboard, BackButton, BaseAdminKeyboard, BaseSuperadminKeyboard
from models import User
from service import DefaultUserService


router = Router()
router.message.filter(IsAdminFilter())


class FSMSuperAdmin(StatesGroup):
    main_menu = State()
    admin_management_menu = State()
    fill_username_to_add = State()
    fill_username_to_delete = State()


class FSMAdmin(StatesGroup):
    main_menu = State()


@router.message(CommandStart())
async def process_admin_start(message: Message, state: FSMContext, user_service: DefaultUserService) -> None:
    user = await user_service.get_one(message.from_user.id)
    if user.is_superuser:
        keyboard = BaseSuperadminKeyboard()()
        await state.set_state(FSMSuperAdmin.main_menu)
    else:
        keyboard = BaseAdminKeyboard()()
        await state.set_state(FSMAdmin.main_menu)
    await message.delete()
    await message.answer(
        text=_(
            "<b>Welcome to the CoverDanceBot admin panel</b>\n\n"
            "Press <b>/help</b> in the menu to see a description of all the actions"
            "available to you.",
        ),
        parse_mode="HTML",
        reply_markup=keyboard,
    )


@router.message(Command(commands="help"), IsSuperAdminFilter())
async def process_super_admin_help_button(message: Message) -> None:
    await message.answer(
        text=_(
            "<b>Superadmin help section</b>\n\n"
            "<b>[🔍Find a practice video]</b> - Perform the video search procedure "
            "according to the specified parameters\n\n"
            "<b>[⚙️Admin management]</b> - Switching to the admin management menu\n\n"
            "<b>[➕Add video]</b> - Adding a new video to the bot's database\n\n"
            "<b>[🈹Change language]</b> - Changing the language of the bot interface",
        ),
    )


@router.message(Command(commands="help"))
async def process_admin_help_button(message: Message) -> None:
    await message.delete()
    await message.answer(
        text=_(
            "<b>Admin help section</b>\n\n"
            "<b>[🔍Find a practice video]</b> - Perform the video search procedure "
            "according to the specified parameters\n\n"
            "<b>[📽️Add video]</b> - Adding a new video to the bot's database\n\n"
            "<b>[🈹Change language]</b> - Changing the language of the bot interface",
        ),
        parse_mode="HTML",
    )


@router.message(lambda m: m.text == _("⚙️Admin management"), StateFilter(FSMSuperAdmin.main_menu))
async def admin_management_menu(message: Message, user_service: DefaultUserService, state: FSMContext) -> None:
    await message.delete()
    await message.answer(
        text=_("List of admins: \n")
        + "\n".join(["@" + str(user.username) for user in await user_service.get() if user.is_staff]),
        reply_markup=AdminManagementInlineKeyboard()(),
    )
    await state.set_state(FSMSuperAdmin.admin_management_menu)


@router.callback_query(F.data == "add_admin_button_pressed", StateFilter(FSMSuperAdmin.admin_management_menu))
async def ask_for_new_admin_name(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        text=_("Pleace enter the username"),
        reply_markup=BackButton()(),
    )
    await state.set_state(FSMSuperAdmin.fill_username_to_add)
    await state.update_data(
        {
            "admin_management_menu_message": {
                "id": callback.id,
                "from_user": callback.from_user,
                "chat_instance": callback.chat_instance,
            },
        },
    )


@router.callback_query(F.data == "delete_admin_button_pressed", StateFilter(FSMSuperAdmin.admin_management_menu))
async def ask_for_delete_admin_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=_("Pleace enter the username"),
        reply_markup=BackButton()(),
    )
    await state.set_state(FSMSuperAdmin.fill_username_to_delete)
    await state.update_data({"admin_management_menu_message": callback})


@router.callback_query(F.data == "back_button_pressed", StateFilter(FSMSuperAdmin.admin_management_menu))
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(FSMSuperAdmin.main_menu)


@router.callback_query(
    F.data == "back_button_pressed",
    StateFilter(FSMSuperAdmin.fill_username_to_add, FSMSuperAdmin.fill_username_to_delete),
)
async def back_to_admin_management_menu(callback: CallbackQuery, state: FSMContext, user_service: DefaultUserService):
    await callback.message.edit_text(
        text=_("List of admins: \n")
        + "\n".join(["@" + str(user.username) for user in await user_service.get() if user.is_staff]),
    )
    await callback.message.edit_reply_markup(reply_markup=AdminManagementInlineKeyboard()())
    await state.set_state(FSMSuperAdmin.admin_management_menu)


@router.message(StateFilter(FSMSuperAdmin.fill_username_to_add))
async def add_admin(message: Message, user_service: DefaultUserService) -> None:
    user = await user_service.get_by_username(message.text.lstrip("@"))
    await message.delete()
    if not user:
        await message.answer(_("Please make sure this user is using a bot or try entering username again"))
    elif user.is_staff:
        await message.answer(text=_("This user is already an admin, try again or press [back]"))
    else:
        await user_service.update_role(user.id, True)
        await message.answer(text=_("Admin successfully added, enter another username or press [back]"))


@router.message(F.text, StateFilter(FSMSuperAdmin.fill_username_to_delete))
async def delete_admin(message: Message, current_user: User, user_service: DefaultUserService) -> None:
    await message.delete()
    user = await user_service.get_by_username(message.text.lstrip("@"))
    if not user:
        await message.answer(_("Please make sure this user is using a bot or try entering username again"))
    elif not user.is_staff:
        await message.answer(text=_("This user is not an admin, try again or press [back]"))
    elif user.id == current_user.id:
        await message.answer(
            text=_("<b>You cannot revoke your administrator rights</b>\n\nEnter another user name or press [back]"),
            parse_mode="HTML",
        )
    else:
        await user_service.update_role(user.id, False)
        await message.answer(text=_("Admin successfully deleted, enter another username or press [back]"))


@router.message()
async def process_any_message(message: Message):
    await message.delete()


__all__ = ["router"]
