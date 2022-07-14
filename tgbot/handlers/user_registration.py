# Процесс регистрации пользователя, ввод имени, описания, номера телефона
from aiogram import types, Router
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.misc.main_router import main_menu
from tgbot.variables_validation.user import *
from tgbot.keyboards.reply.reply import without_number_phone_keyboard, remove_keyboard
from tgbot.database.database import Database
from tgbot.database.schemas import User, UserProfile
from tgbot.misc.states import UserRegistration

user_registration_router = Router()


@user_registration_router.message(state='*', commands=['start'])
async def start(message: types.Message, state: FSMContext, db: Database):
    await User().load_from_tg_user(message.from_user).save(db)

    if await db.is_user_registered(message.from_user.id):
        await main_menu(message, state)
    else:
        await message.answer('Введите свое имя...', reply_markup=remove_keyboard)
        await state.set_state(UserRegistration.name)


# Принимаем имя пользователя
@user_registration_router.message(state=UserRegistration.name)
async def take_name(message: types.Message, state: FSMContext):
    name = message.text

    if await name_is_valid(name, message):
        await state.update_data(name=name)
        await state.set_state(UserRegistration.age)
        await message.answer('Введите свой возраст...')


# Принимаем имя пользователя
@user_registration_router.message(state=UserRegistration.age)
async def take_age(message: types.Message, state: FSMContext):
    age = message.text

    if await age_is_valid(age, message):
        await state.update_data(age=age)
        await state.set_state(UserRegistration.description)
        await message.answer('Напишите пару слов о себе...')


# Принимаем описание пользователя
@user_registration_router.message(state=UserRegistration.description)
async def take_description(message: types.Message, state: FSMContext):
    description = message.text

    if await description_is_valid(description, message):
        await state.update_data(description=description)
        await state.set_state(UserRegistration.phone_number)
        await message.answer('Введите свой номер телефона...', reply_markup=without_number_phone_keyboard)


# Принимаем номер телефона пользователя
@user_registration_router.message(state=UserRegistration.phone_number)
async def take_phone_number(message: types.Message, db: Database, state: FSMContext):
    phone_number = message.text

    if phone_number == without_number_phone_keyboard.keyboard[0][0].text:
        phone_number = None

    if await phone_number_is_valid(phone_number, message):
        await state.update_data(phone_number=phone_number, user_id=message.from_user.id)
        data = await state.get_data()
        await UserProfile().load_from_data(data).save(db)
        await message.answer('Вы успешно зарегистрировались!')
        await main_menu(message, state)

