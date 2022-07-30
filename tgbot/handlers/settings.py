# Процесс изменения профиля пользователя

from aiogram import types, Router, Bot, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.database.database import Database
from tgbot.database.schemas import UserProfile
from tgbot.filters.main_menu import MyProfileFilter, SettingsFilter
from tgbot.handlers import commands_router
from tgbot.keyboards.inline.my_profile import my_profile_keyboard, MyProfileCD
from tgbot.keyboards.inline.settings import notifications_true_keyboard, notifications_false_keyboard, SettingsCD
from tgbot.misc.main_router import main_menu
from tgbot.misc.states import MyProfile, Settings
from tgbot.misc.templates import get_user_self_template
from tgbot.validation.order import *
from tgbot.keyboards.reply.reply import *

from tgbot.validation.user import age_is_valid, phone_number_is_valid
from tgbot.misc import replicas

settings_router = Router()


@commands_router.message(SettingsFilter())
async def start(message: types.Message, state: FSMContext, db: Database):
    user_profile = await db.get_user_profile_by_id(message.from_user.id)

    if user_profile.notifications:
        await message.answer('✅ Уведомления о новых заказах включены', reply_markup=notifications_true_keyboard)
    else:
        await message.answer('❌ Уведомления о новых заказах выключены', reply_markup=notifications_false_keyboard)

    await state.set_state(Settings.action)


@settings_router.callback_query(SettingsCD.filter(F.states_group == 'settings'), state=Settings.action)
async def take_action(call: CallbackQuery, state: FSMContext, callback_data: SettingsCD, db: Database):
    if callback_data.value == 'off':
        await db.alter_user(call.from_user.id, notifications=False)
        await call.message.edit_text('❌ Уведомления о новых заказах выключены', reply_markup=notifications_false_keyboard)

    elif callback_data.value in ['on', 'update']:
        await call.message.delete()
        await call.message.answer(replicas.user_registration.location, reply_markup=send_self_geoposition)
        await state.set_state(Settings.location)

    elif callback_data.value == 'back':
        await call.message.delete()
        await main_menu(call.message, state)


@settings_router.message(state=Settings.location, content_types=['location'])
async def take_location(message: Message, state: FSMContext, db: Database):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await db.alter_user(message.from_user.id, latitude=latitude, longitude=longitude, notifications=True)
    await start(message, state, db)


@settings_router.message(state=Settings.location)
async def take_false_location(message: Message, state: FSMContext, db: Database):
    await message.answer(replicas.user_registration.location, reply_markup=send_self_geoposition)










