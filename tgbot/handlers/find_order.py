# Процесс поиска заказов

from aiogram import types, Router, Bot, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.database.database import Database
from tgbot.filters.main_menu import FindOrderFilter
from tgbot.handlers import commands_router
from tgbot.keyboards.inline.inline import get_order_keyboard, continue_order_finding_keyboard, FindOrderCD
from tgbot.misc.orders_searching import find_nearest_orders
from tgbot.misc.states import FindOrder
from tgbot.misc.templates import get_order_template, get_user_template
from tgbot.keyboards.reply.reply import *

find_order_router = Router()


@commands_router.message(FindOrderFilter())
async def start(message: types.Message, state: FSMContext):
    await message.answer('Отправьте свою геопозицию, чтобы мы могли найти наиболее близкие для вас заказы...',
                         reply_markup=send_self_geoposition)
    await state.set_state(FindOrder.location)


# Принимаем геопозицию пользователя
@find_order_router.message(state=FindOrder.location, content_types=['location'])
async def take_geoposition(message: types.Message, state: FSMContext, db: Database, bot: Bot):
    latitude = message.location.latitude
    longitude = message.location.longitude

    await state.update_data(latitude=latitude, longitude=longitude, viewed_orders=[])
    await state.set_state(FindOrder.order)

    status = await send_next_order(bot, state, db, message)

    if status == 'no_orders':
        await state.set_state(FindOrder.location)
        await message.answer('Пока доступных заказов нет (( Попробуйте подождать или обновить свою геопозицию ',
                             reply_markup=send_self_geoposition)


# Принимаем геопозицию пользователя
@find_order_router.callback_query(FindOrderCD.filter(F.states_group == 'find_order'), state=FindOrder.order)
async def take_order_decision(call: types.CallbackQuery, state: FSMContext, callback_data: FindOrderCD, bot: Bot, db: Database):
    data = await state.get_data()

    if callback_data.value == 'skip':
        await delete_previous_messages(data, bot, call)
        status = await send_next_order(bot, state, db, call.message)

        if status == 'no_orders':
            await state.set_state(FindOrder.location)
            await call.message.answer('Больше доступных заказов нет(( Попробуйте обновить свою геопозицию...',
                                      reply_markup=send_self_geoposition)

    elif callback_data.value == 'accept':
        order = data['order']

        if await db.check_order_availability(order.id):
            await call.message.edit_reply_markup(reply_markup=None)
            await db.alter_order(order.id, status=2, executor_id=call.from_user.id)

            executor_profile = await db.get_user_profile_by_id(call.from_user.id)
            creator_profile = await db.get_user_profile_by_id(order.creator_id)

            await state.clear()
            await call.message.answer(get_user_template(creator_profile, 'creator'), reply_markup=main_menu_keyboard)
            await bot.send_message(order.creator_id, get_user_template(executor_profile, 'executor', order.name))

        else:
            await delete_previous_messages(data, bot, call)
            await call.message.answer(f'Извиняемся! Данный заказ уже взял другой исполнитель.',
                                      reply_markup=continue_order_finding_keyboard)


async def delete_previous_messages(data, bot, call):
    for photo_message in data['photo_messages']:
        await bot.delete_message(chat_id=photo_message.chat.id, message_id=photo_message.message_id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


# Отправить пользователю заказ
async def send_next_order(bot: Bot, state: FSMContext, db: Database, message: Message):
    data = await state.get_data()
    viewed_orders = data['viewed_orders']
    user_location = (data['latitude'], data['longitude'])

    nearest_orders = await find_nearest_orders(db, user_location, message.from_user.id)
    nearest_orders_gen = (i for i in nearest_orders)

    while True:
        try:
            order_row = next(nearest_orders_gen)
        except StopIteration:
            return 'no_orders'

        if order_row[0] not in viewed_orders:
            break

    order = await db.get_order_by_id(order_row[0])
    viewed_orders.append(order.id)
    await state.update_data(order=order, viewed_orders=viewed_orders)

    reply_markup = get_order_keyboard(order)
    text, photos = get_order_template(order)
    text += f'\n<b>Расстояние до вас:</b> {round(order_row[1], 2)} км.'

    photo_messages = []
    if len(photos) != 0:
        photo_messages = await bot.send_media_group(chat_id=message.chat.id, media=photos)

    await state.update_data(photo_messages=photo_messages)
    await message.answer(text, reply_markup=reply_markup)




















