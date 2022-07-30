# Процесс регистрации пользователя, ввод имени, описания, номера телефона
from aiogram import types, Router, Bot
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.handlers import commands_router
from tgbot.misc.main_router import main_menu
from tgbot.validation.user import *
from tgbot.keyboards.reply.reply import without_number_phone_keyboard, remove_keyboard, \
    without_user_description_keyboard, notifications_decision_keyboard, send_self_geoposition
from tgbot.database.database import Database
from tgbot.database.schemas import User, UserProfile
from tgbot.misc.states import UserRegistration
from tgbot.misc import replicas

user_registration_router = Router()


@commands_router.message(state='*', commands=['start'])
async def start(message: types.Message, state: FSMContext, db: Database):
    await User().load_from_tg_user(message.from_user).save(db)

    if await db.is_user_registered(message.from_user.id):
        await main_menu(message, state)
    else:
        await message.answer(replicas.user_registration.name, reply_markup=remove_keyboard)
        await state.set_state(UserRegistration.name)


# Принимаем имя пользователя
@user_registration_router.message(state=UserRegistration.name)
async def take_name(message: types.Message, state: FSMContext):
    name = message.text

    if await name_is_valid(name, message):
        await state.update_data(name=name)
        await state.set_state(UserRegistration.age)
        await message.answer(replicas.user_registration.age)


# Принимаем имя пользователя
@user_registration_router.message(state=UserRegistration.age)
async def take_age(message: types.Message, state: FSMContext):
    age = message.text

    if await age_is_valid(age, message):
        await state.update_data(age=age)
        await state.set_state(UserRegistration.phone_number)
        await message.answer(replicas.user_registration.phone_number,
                             reply_markup=without_number_phone_keyboard)


# Принимаем номер телефона пользователя
@user_registration_router.message(state=UserRegistration.phone_number)
async def take_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text

    if phone_number == without_number_phone_keyboard.keyboard[0][0].text:
        phone_number = None

    if await phone_number_is_valid(phone_number, message):
        await state.update_data(phone_number=phone_number)
        await state.set_state(UserRegistration.description)
        await message.answer(replicas.user_registration.description,
                             reply_markup=without_user_description_keyboard)


# Принимаем описание пользователя
@user_registration_router.message(state=UserRegistration.description)
async def take_description(message: types.Message, state: FSMContext):
    description = message.text

    if description == without_user_description_keyboard.keyboard[0][0].text:
        description = None

    if await description_is_valid(description, message):
        await state.update_data(description=description)
        await state.set_state(UserRegistration.notifications)
        await message.answer(replicas.user_registration.notifications,
                             reply_markup=notifications_decision_keyboard)


# Принимаем решение об отправке уведомлений
@user_registration_router.message(state=UserRegistration.notifications)
async def take_notifications_decision(message: types.Message, db: Database, state: FSMContext):
    decision = message.text

    if await notifications_decision_is_valid(decision, message):
        if decision == notifications_decision_keyboard.keyboard[0][0].text:
            await state.update_data(notifications=True)
            await state.set_state(UserRegistration.location)
            await message.answer(replicas.user_registration.location, reply_markup=send_self_geoposition)

        elif decision == notifications_decision_keyboard.keyboard[0][1].text:
            await state.update_data(notifications=False)
            await end(message, state, db)


# Принимаем геопозицию заказа
@user_registration_router.message(state=UserRegistration.location, content_types=['location'])
async def take_geoposition(message: types.Message, state: FSMContext, db: Database):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await state.update_data(latitude=latitude, longitude=longitude)
    await end(message, state, db)


# Принимаем ложную геопозицию заказа
@user_registration_router.message(state=UserRegistration.location)
async def take_geoposition(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer(replicas.user_registration.location, reply_markup=send_self_geoposition)


async def end(message, state, db):
    await state.update_data(user_id=message.from_user.id)
    data = await state.get_data()
    await UserProfile().load_from_data(data).save(db)
    await message.answer('Вы успешно зарегистрировались! \n'
                         'Изменить профиль и настроить уведомления вы можете в настройках \n'
                         '/settings')
    await main_menu(message, state)