from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _
from datetime import datetime


from filters import IsAdminFilter, IsSuperAdminFilter
from keyboards import (
    AdminManagementInlineKeyboard,
    BackButton,
    BaseAdminKeyboard,
    BaseSuperadminKeyboard,
    ChooseDifficultKeyboard,
    ChooseGenderKeyboard,
    SaveCoverKeyboard,
)
from models import User
from service import DefaultUserService, DefaultCoverService
from repository import CoverDataClass
from models import DifficultEnum


router = Router()
router.message.filter(IsAdminFilter())


class FSMSuperAdmin(StatesGroup):
    main_menu = State()
    admin_management_menu = State()
    fill_username_to_add = State()
    fill_username_to_delete = State()


class FSMAdmin(StatesGroup):
    main_menu = State()
    fill_cover_name = State()
    fil_cover_url = State()
    fill_cover_gender = State()
    fill_cover_members = State()
    fill_cover_difficulty = State()
    fill_cover_publish_date = State()
    save_cover = State()


@router.message(CommandStart())
async def process_admin_start(message: Message, state: FSMContext, user_service: DefaultUserService) -> None:
    await message.delete()
    await state.clear()
    user = await user_service.get_one(message.from_user.id)
    if user.is_superuser:
        keyboard = BaseSuperadminKeyboard()()
        await state.set_state(FSMSuperAdmin.main_menu)
    else:
        keyboard = BaseAdminKeyboard()()
        await state.set_state(FSMAdmin.main_menu)
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
        id=callback.id,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )


@router.callback_query(F.data == "delete_admin_button_pressed", StateFilter(FSMSuperAdmin.admin_management_menu))
async def ask_for_delete_admin_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=_("Pleace enter the username"),
        reply_markup=BackButton()(),
    )
    await state.set_state(FSMSuperAdmin.fill_username_to_delete)
    await state.update_data(
        id=callback.id,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )


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
async def add_admin(message: Message, user_service: DefaultUserService, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    user = await user_service.get_by_username(message.text.lstrip("@"))
    await message.delete()
    if not user:
        await bot.answer_callback_query(
            callback_query_id=data["id"],
            text=_("Please make sure this user is using a bot or try entering username again"),
            show_alert=True,
        )
    elif user.is_staff:
        await bot.answer_callback_query(
            callback_query_id=data["id"],
            text=_("This user is already an admin, try again or press [back]"),
            show_alert=True,
        )
    else:
        await user_service.update_role(user.id, True)
        await bot.answer_callback_query(
            callback_query_id=data["id"],
            text=_("Admin successfully added"),
            show_alert=True,
        )
        await bot.edit_message_text(
            chat_id=data["chat_id"],
            message_id=data["message_id"],
            text=_("List of admins: \n")
            + "\n".join(["@" + str(user.username) for user in await user_service.get() if user.is_staff]),
            reply_markup=AdminManagementInlineKeyboard()(),
        )
        await state.clear()
        await state.set_state(FSMSuperAdmin.admin_management_menu)


@router.message(StateFilter(FSMSuperAdmin.fill_username_to_delete))
async def delete_admin(
    message: Message,
    current_user: User,
    user_service: DefaultUserService,
    state: FSMContext,
    bot: Bot,
) -> None:
    data = await state.get_data()
    await message.delete()
    user = await user_service.get_by_username(message.text.lstrip("@"))
    if not user:
        await bot.answer_callback_query(
            callback_query_id=data["id"],
            text=_("Please make sure this user is using a bot or try entering username again"),
            show_alert=True,
        )
    elif not user.is_staff:
        await bot.answer_callback_query(
            callback_query_id=data["id"],
            text=_("This user is not an admin, try again or press [back]"),
            show_alert=True,
        )
    elif user.id == current_user.id:
        await bot.answer_callback_query(
            callback_query_id=data["id"],
            text=_("You cannot revoke your administrator rights\n\nEnter another username or press [back]"),
            show_alert=True,
        )
    else:
        await user_service.update_role(user.id, False)
        await bot.answer_callback_query(
            callback_query_id=data["id"],
            text=_("Admin successfully deleted"),
            show_alert=True,
        )
        await bot.edit_message_text(
            chat_id=data["chat_id"],
            message_id=data["message_id"],
            text=_("List of admins: \n")
            + "\n".join(["@" + str(user.username) for user in await user_service.get() if user.is_staff]),
            reply_markup=AdminManagementInlineKeyboard()(),
        )
        await state.clear()
        await state.set_state(FSMSuperAdmin.admin_management_menu)


@router.message(lambda m: m.text == _("📽️Add video"), StateFilter(FSMSuperAdmin.main_menu, FSMAdmin.main_menu))
async def process_add_video_button(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(text=_("Please enter the name of the cover"))
    await state.set_state(FSMAdmin.fill_cover_name)


@router.message(StateFilter(FSMAdmin.fill_cover_name))
async def process_cover_name_input(message: Message, state: FSMContext):
    await message.answer(text=_("Please enter the link to the cover"))
    await state.update_data(cover_name=message.text)
    await state.set_state(FSMAdmin.fil_cover_url)


@router.message(StateFilter(FSMAdmin.fil_cover_url))
async def process_cover_url_input(message: Message, state: FSMContext):
    await message.answer(text=_("Select gender"), reply_markup=ChooseGenderKeyboard()())
    await state.update_data(cover_url=message.text)
    await state.set_state(FSMAdmin.fill_cover_gender)


@router.message(StateFilter(FSMAdmin.fill_cover_gender))
async def process_cover_gender_input(message: Message, state: FSMContext):
    await message.answer(text=_("Enter the number of participants"))
    if message.text == _("Female"):
        await state.update_data(cover_gender=False)
    else:
        await state.update_data(cover_gender=True)
    await state.set_state(FSMAdmin.fill_cover_members)


@router.message(StateFilter(FSMAdmin.fill_cover_members))
async def process_cover_members_input(message: Message, state: FSMContext):
    await message.answer(text=_("Choose difficulty level"), reply_markup=ChooseDifficultKeyboard()())
    await state.update_data(cover_members=message.text)
    await state.set_state(FSMAdmin.fill_cover_difficulty)


@router.message(StateFilter(FSMAdmin.fill_cover_difficulty))
async def process_cover_difficulty_input(message: Message, state: FSMContext):
    await message.answer(text=_("Enter the date of publication of the cover in the format of YYYY-MM-DD"))
    if message.text == _("Easy"):
        await state.update_data(cover_difficulty="easy")
    else:
        await state.update_data(cover_difficulty="hard")
    await state.set_state(FSMAdmin.fill_cover_publish_date)


@router.message(StateFilter(FSMAdmin.fill_cover_publish_date))
async def process_cover_publish_date_input(message: Message, state: FSMContext):
    await state.update_data(cover_publish_date=message.text)
    cover_data = await state.get_data()
    await message.answer(
        text=_(
            "<b>Please check the data entered:</b>\n\n"
            + "Cover name: {}\n"
            + "Cover url: {}\n"
            + "Cover gender: {}\n"
            + "Cover members count: {}\n"
            + "Cover difficulty: {}\n"
            + "Cover publish date: {}",
        ).format(
            cover_data["cover_name"],
            cover_data["cover_url"],
            _("Male") if cover_data["cover_gender"] else "Female",
            cover_data["cover_members"],
            _(cover_data["cover_difficulty"].capitalize()),
            message.text.replace("-", "."),
        ),
        reply_markup=SaveCoverKeyboard()(),
        parse_mode="HTML",
    )
    await state.set_state(FSMAdmin.save_cover)


@router.message(StateFilter(FSMAdmin.save_cover))
async def process_cover_save(
    message: Message,
    state: FSMContext,
    cover_service: DefaultCoverService,
    current_user: User,
):
    keyboard = BaseSuperadminKeyboard()() if current_user.is_superuser else BaseAdminKeyboard()()
    if message.text == _("✅Save cover"):
        cover_data = await state.get_data()
        try:
            cover = CoverDataClass(
                author_id=message.from_user.id,
                name=cover_data["cover_name"],
                url=cover_data["cover_url"],
                gender=cover_data["cover_gender"],
                members=int(cover_data["cover_members"]),
                difficult=DifficultEnum(cover_data["cover_difficulty"]),
                publish_date=datetime.strptime(cover_data["cover_publish_date"], "%Y-%m-%d").date(),
            )
            await cover_service.create(cover_data=cover)
            await message.answer(
                text=_("<b>Cover has been added to the database</b>"),
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            await state.clear()
            if current_user.is_superuser:
                await state.set_state(FSMSuperAdmin.main_menu)
            elif current_user.is_staff:
                await state.set_state(FSMAdmin.main_menu)
        except Exception:
            await state.clear()
            await state.set_state(FSMAdmin.fill_cover_name)
            await message.answer(
                text=_("<b>Failed to add the cover to the database.</b>\n\n<b>Please try entering the data again</b>"),
                parse_mode="HTML",
            )
            await message.answer(text=_("Please enter the name of the cover"))
    elif message.text == _("🔄️Redo the cover form"):
        await state.clear()
        await state.set_state(FSMAdmin.fill_cover_name)
        await message.answer(text=_("Please enter the name of the cover"))
    elif message.text == _("❌Don't save the cover"):
        await state.clear()
        if current_user.is_superuser:
            await state.set_state(FSMSuperAdmin.main_menu)
        elif current_user.is_staff:
            await state.set_state(FSMAdmin.main_menu)
        await message.answer(text=_("<b>The changes are cancelled</b>"), reply_markup=keyboard, parse_mode="HTML")


@router.message()
async def process_any_message(message: Message):
    await message.delete()


__all__ = ["router"]
