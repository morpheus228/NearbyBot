# Процесс изменения профиля пользователя

from aiogram import types, Router, Bot, F
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.database.database import Database
from tgbot.database.schemas import UserProfile
from tgbot.filters.main_menu import MyProfileFilter
from tgbot.handlers import commands_router
from tgbot.keyboards.inline.my_profile import my_profile_keyboard, MyProfileCD
from tgbot.misc.main_router import main_menu
from tgbot.misc.states import MyProfile
from tgbot.misc.templates import get_user_self_template
from tgbot.validation.order import *
from tgbot.keyboards.reply.reply import *

from tgbot.validation.user import age_is_valid, phone_number_is_valid
from tgbot.misc import replicas

my_profile_router = Router()


@commands_router.message(MyProfileFilter())
async def start(message: types.Message, state: FSMContext, db: Database):
    user_profile = await db.get_user_profile_by_id(message.from_user.id)
    text = get_user_self_template(user_profile)
    text += '\n\nВы можете изменить:'
    await message.answer(text, reply_markup=my_profile_keyboard)
    await state.set_state(MyProfile.action)


@my_profile_router.callback_query(MyProfileCD.filter(F.states_group == 'my_profile'), state=MyProfile.action)
async def take_action(call: types.CallbackQuery, callback_data: MyProfileCD, state: FSMContext, bot: Bot):
    await bot.delete_message(call.message.chat.id, call.message.message_id)

    if callback_data.value == 'name':
        await call.message.answer(replicas.user_registration.name, reply_markup=remove_keyboard)
        await state.set_state(MyProfile.name)
        await state.update_data(action='name')

    elif callback_data.value == 'age':
        await call.message.answer(replicas.user_registration.age, reply_markup=remove_keyboard)
        await state.set_state(MyProfile.age)
        await state.update_data(action='age')

    elif callback_data.value == 'phone_number':
        await call.message.answer(replicas.user_registration.phone_number, reply_markup=without_number_phone_keyboard)
        await state.set_state(MyProfile.phone_number)
        await state.update_data(action='phone_number')

    elif callback_data.value == 'description':
        await call.message.answer(replicas.user_registration.description, reply_markup=without_user_description_keyboard)
        await state.set_state(MyProfile.description)
        await state.update_data(action='description')

    elif callback_data.value == 'full':
        await call.message.answer(replicas.user_registration.name, reply_markup=remove_keyboard)
        await state.set_state(MyProfile.name)
        await state.update_data(action='full')

    elif callback_data.value == 'back':
        await main_menu(call.message, state)


# Принимаем имя пользователя
@my_profile_router.message(state=MyProfile.name)
async def take_name(message: types.Message, state: FSMContext, db: Database):
    name = message.text
    action = (await state.get_data())['action']

    if await name_is_valid(name, message):

        if action == 'full':
            await state.update_data(name=name)
            await state.set_state(MyProfile.age)
            await message.answer(replicas.user_registration.age)

        else:
            await db.alter_user(message.from_user.id, name=name)
            await message.answer(replicas.my_profile.name_successfully, reply_markup=main_menu_keyboard)
            await state.clear()


# Принимаем имя пользователя
@my_profile_router.message(state=MyProfile.age)
async def take_age(message: types.Message, state: FSMContext, db: Database):
    age = message.text
    action = (await state.get_data())['action']

    if await age_is_valid(age, message):

        if action == 'full':
            await state.update_data(age=age)
            await state.set_state(MyProfile.phone_number)
            await message.answer(replicas.user_registration.phone_number, reply_markup=without_number_phone_keyboard)

        else:
            await db.alter_user(message.from_user.id, age=age)
            await message.answer(replicas.my_profile.age_successfully, reply_markup=main_menu_keyboard)
            await state.clear()


# Принимаем номер телефона пользователя
@my_profile_router.message(state=MyProfile.phone_number)
async def take_phone_number(message: types.Message, db: Database, state: FSMContext):
    phone_number = message.text
    action = (await state.get_data())['action']

    if phone_number == without_number_phone_keyboard.keyboard[0][0].text:
        phone_number = None

    if await phone_number_is_valid(phone_number, message):

        if action == 'full':
            await state.update_data(phone_number=phone_number)
            await state.set_state(MyProfile.description)
            await message.answer(replicas.user_registration.description, reply_markup=without_user_description_keyboard)

        else:
            await db.alter_user(message.from_user.id, phone_number=phone_number)
            await message.answer(replicas.my_profile.phone_number_successfully, reply_markup=main_menu_keyboard)
            await state.clear()


# Принимаем описание пользователя
@my_profile_router.message(state=MyProfile.description)
async def take_description(message: types.Message, state: FSMContext, db: Database):
    description = message.text
    action = (await state.get_data())['action']

    if description == without_user_description_keyboard.keyboard[0][0].text:
        description = None

    if await description_is_valid(description, message):

        if action == 'full':
            await state.update_data(description=description, user_id=message.from_user.id)
            data = await state.get_data()
            await UserProfile().load_from_data(data).save(db)
            await message.answer(replicas.my_profile.profile_successfully, reply_markup=main_menu_keyboard)
            await state.clear()

        else:
            await db.alter_user(message.from_user.id, description=description)
            await message.answer(replicas.my_profile.description_successfully, reply_markup=main_menu_keyboard)
            await state.clear()