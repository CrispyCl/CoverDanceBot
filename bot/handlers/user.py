from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from keyboards import ChooseDifficultKeyboard, ChooseGenderToSearchKeyboard, CoverViewKeyboard, MainUserKeyboard
from models import User
from service import DefaultCoverService, DefaultUserService


router = Router()


class FSMUser(StatesGroup):
    main_menu = State()
    fill_gender_to_search = State()
    fill_year_to_search = State()
    fill_members_to_search = State()
    fill_difficulty_to_search = State()
    view_cover = State()


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
    current_user = await user_service.get_one(current_user.id)
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


@router.message(
    lambda m: m.text == _("🔍Find practice video"),
    StateFilter(FSMUser.main_menu),
)
async def process_find_video_button(
    message: Message,
    user_service: DefaultUserService,
    current_user: User,
    state: FSMContext,
):
    if current_user.token_count < 1000:
        await message.answer(
            text=_(
                "<b><i>Ooooops!</i></b>\n\n<b>You don't have enough tokens to search for videos</b>\n\n"
                "Press [💰Balance] to find out how you can get tokens",
            ),
        )
    else:
        await user_service.update_token(current_user.id, -1000)
        await message.answer(text=_("Choose gender"), reply_markup=ChooseGenderToSearchKeyboard()())
        await state.set_state(FSMUser.fill_gender_to_search)


@router.message(StateFilter(FSMUser.fill_gender_to_search))
async def process_gender_search_input(message: Message, state: FSMContext):
    await message.answer(
        text=_("Enter a range of years to search for videos in YYYY-YYYY format"),
        reply_markup=ReplyKeyboardRemove(),
    )
    if message.text == _("Male"):
        await state.update_data(gender_to_search=True)
    elif message.text == _("Female"):
        await state.update_data(gender_to_search=False)
    else:
        await state.update_data(gender_to_search=None)
    await state.set_state(FSMUser.fill_year_to_search)


@router.message(StateFilter(FSMUser.fill_year_to_search))
async def process_year_search_input(message: Message, state: FSMContext):
    try:
        years = message.text.split("-")
        if (2000 <= int(years[0]) <= 2025) and (2000 <= int(years[1]) <= 2025):
            await message.answer(text=_("Enter the number of participants"))
            await state.update_data(start_year_to_search=int(years[0]), end_year_to_search=int(years[1]))
            await state.set_state(FSMUser.fill_members_to_search)
        else:
            await message.answer(
                text=_(
                    "<b>Invalid range entered</b>\n\n" "Try entering the video search time range again",
                ),
                parse_mode="HTML",
            )
    except Exception:
        await message.answer(
            text=_(
                "<b>Invalid range entered</b>\n\n" "Try entering the video search time range again",
            ),
            parse_mode="HTML",
        )


@router.message(StateFilter(FSMUser.fill_members_to_search))
async def process_members_search_input(message: Message, state: FSMContext):
    try:
        members = int(message.text)
        if members < 3:
            await message.answer(
                text=_(
                    "<b>The number of participants in the cover may not be less than 3</b>\n\n"
                    "Please specify the number of participants again",
                ),
                parse_mode="HTML",
            )
        elif members > 9:
            await state.update_data(members_to_search=10)
            await state.set_state(FSMUser.fill_difficulty_to_search)
            await message.answer(text=_("Choose the cover difficulty level"), reply_markup=ChooseDifficultKeyboard()())
        else:
            await state.update_data(members_to_search=int(message.text))
            await state.set_state(FSMUser.fill_difficulty_to_search)
            await message.answer(text=_("Choose the cover difficulty level"), reply_markup=ChooseDifficultKeyboard()())
    except Exception:
        await message.answer(
            text=_(
                "<b>The number of participants in the cover may not be less than 3</b>\n\n"
                "Please specify the number of participants again",
            ),
            parse_mode="HTML",
        )


@router.message(StateFilter(FSMUser.fill_difficulty_to_search))
async def process_difficulty_search(
    message: Message,
    user_service: DefaultUserService,
    current_user: User,
    cover_service: DefaultCoverService,
    state: FSMContext,
):
    if message.text == "Высокий":
        await state.update_data(difficulty_to_search="hard")
    elif message.text == "Средний":
        await state.update_data(difficulty_to_search="middle")
    elif message.text == "Низкий":
        await state.update_data(difficulty_to_search="easy")
    search_data = await state.get_data()
    covers = await cover_service.find(
        gender=search_data["gender_to_search"],
        members=search_data["members_to_search"],
        difficult=search_data["difficulty_to_search"],
        start_year=search_data["start_year_to_search"],
        end_year=search_data["end_year_to_search"],
    )
    if len(covers) > 0:
        await message.answer(text=_("Found the videos:"), reply_markup=CoverViewKeyboard()())
        for i in range(len(covers) if len(covers) < 3 else 3):
            await message.answer(
                text=_("Name: {}\nGender: {}\nURL: {}").format(
                    covers[i].name,
                    _("Male") if covers[i].gender else _("Female"),
                    covers[i].url,
                ),
            )
        await state.update_data(last_viewed_cover=2)
        await state.set_state(FSMUser.view_cover)
    else:
        await message.answer(
            text=_("Sorry, no videos were found for this request"),
            reply_markup=MainUserKeyboard()(),
        )
        await user_service.update_token(current_user.id, 1000)
        await state.clear()
        await state.set_state(FSMUser.main_menu)


@router.message(StateFilter(FSMUser.view_cover))
async def process_view_cover_menu(
    message: Message,
    user_service: DefaultUserService,
    cover_service: DefaultCoverService,
    current_user: User,
    state: FSMContext,
):
    if message.text == _("🔍Find more videos"):
        if current_user.token_count < 500:
            await message.answer(
                text=_(
                    "<b><i>Ooooops!</b></i>\n\n<b>You don't have enough tokens to search for more videos</b>\n\n"
                    "Press [💰Balance] to find out how you can get tokens",
                ),
                reply_markup=MainUserKeyboard()(),
            )
            await state.clear()
            await state.set_state(FSMUser.main_menu)
        else:
            search_data = await state.get_data()
            last = search_data["last_viewed_cover"]
            covers = await cover_service.find(
                gender=search_data["gender_to_search"],
                members=search_data["members_to_search"],
                difficult=search_data["difficulty_to_search"],
                start_year=search_data["start_year_to_search"],
                end_year=search_data["end_year_to_search"],
            )
            if len(covers) > last + 1:
                await message.answer(
                    text=_("Another one video found for you:\n\nName: {}\nGender: {}\nURL: {}").format(
                        covers[last + 1].name,
                        covers[last + 1].gender,
                        covers[last + 1].url,
                    ),
                )
                await user_service.update_token(current_user.id, -500)
                await state.update_data(last_viewed_cover=last + 1)
            else:
                await message.answer(
                    text=_("Sorry, no more videos were found for this request"),
                    reply_markup=MainUserKeyboard()(),
                )
                await state.clear()
                await state.set_state(FSMUser.main_menu)
    elif message.text == _("🔙Back to menu"):
        await message.answer(
            text=_("🔙Quit video search"),
            reply_markup=MainUserKeyboard()(),
        )
        await state.clear()
        await state.set_state(FSMUser.main_menu)


@router.message()
async def process_any_invalid_message(message: Message):
    await message.delete()


__all__ = ["router"]
