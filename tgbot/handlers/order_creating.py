# Процесс создания нового заказа

from aiogram import types, Router, Bot
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.database.database import Database
from tgbot.filters.main_menu import NewOrderFilter
from tgbot.filters.order_creating import WithoutPhotoFilter
from tgbot.misc.main_router import main_menu
from tgbot.misc.states import OrderCreating
from tgbot.misc.templates import get_order_template
from tgbot.variables_validation.order import *
from tgbot.keyboards.reply.reply import *

from tgbot.misc.underground import find_nearest_underground

order_creating_router = Router()


@order_creating_router.message(NewOrderFilter())
async def start(message: types.Message, state: FSMContext):
    await message.answer('Введите название заказа...', reply_markup=remove_keyboard)
    await state.set_state(OrderCreating.name)


# Принимаем название заказа
@order_creating_router.message(state=OrderCreating.name)
async def take_name(message: types.Message, state: FSMContext):
    name = message.text

    if await name_is_valid(name, message):
        await state.update_data(name=name)
        await state.set_state(OrderCreating.description)
        await message.answer('Введите подробное описание заказа...', reply_markup=without_description_keyboard)


# Принимаем описание заказа
@order_creating_router.message(state=OrderCreating.description)
async def take_description(message: types.Message, state: FSMContext):
    description = message.text

    if description == without_description_keyboard.keyboard[0][0].text:
        description = None

    if await description_is_valid(description, message):
        await state.update_data(description=description)
        await state.set_state(OrderCreating.first_photo)
        await message.answer('Добавьте фотографии к заказу...', reply_markup=without_photo_keyboard)


# Принимаем отказ от добавления фотографий заказа
@order_creating_router.message(WithoutPhotoFilter())
async def take_without_photo(message: types.Message, state: FSMContext):
    await state.set_state(OrderCreating.price)
    await message.answer('Введите цену заказа...', reply_markup=remove_keyboard)


# Принимаем первую фотографию заказа
@order_creating_router.message(content_types=['photo'], state=OrderCreating.first_photo)
async def take_first_photo(message: types.Message, state: FSMContext):
    if 'first_photo' not in await state.get_data():
        first_photo = message.photo[-1].file_id
        await state.update_data(photo_1=first_photo)
        await state.set_state(OrderCreating.second_photo)
        await message.answer('Фото добавлено - 1 из 6. Добавьте следующую...',
                             reply_markup=stop_photo_adding_keyboard)


# Принимаем вторую фотографию заказа
@order_creating_router.message(content_types=['photo'], state=OrderCreating.second_photo)
async def take_second_photo(message: types.Message, state: FSMContext):
    if 'second_photo' not in await state.get_data():
        second_photo = message.photo[-1].file_id
        await state.update_data(photo_2=second_photo)
        await state.set_state(OrderCreating.third_photo)
        await message.answer('Фото добавлено - 2 из 6. Добавьте следующую...',
                             reply_markup=stop_photo_adding_keyboard)


# Принимаем третью фотографию заказа
@order_creating_router.message(content_types=['photo'], state=OrderCreating.third_photo)
async def take_third_photo(message: types.Message, state: FSMContext):
    if 'third_photo' not in await state.get_data():
        third_photo = message.photo[-1].file_id
        await state.update_data(photo_3=third_photo)
        await state.set_state(OrderCreating.fourth_photo)
        await message.answer('Фото добавлено - 3 из 6. Добавьте следующую...')


# Принимаем четвертую фотографию заказа
@order_creating_router.message(content_types=['photo'], state=OrderCreating.fourth_photo)
async def take_fourth_photo(message: types.Message, state: FSMContext):
    if 'fourth_photo' not in await state.get_data():
        fourth_photo = message.photo[-1].file_id
        await state.update_data(photo_4=fourth_photo)
        await state.set_state(OrderCreating.fifth_photo)
        await message.answer('Фото добавлено - 4 из 6. Добавьте следующую...')


# Принимаем пятую фотографию заказа
@order_creating_router.message(content_types=['photo'], state=OrderCreating.fifth_photo)
async def take_fifth_photo(message: types.Message, state: FSMContext):
    if 'fifth_photo' not in await state.get_data():
        fifth_photo = message.photo[-1].file_id
        await state.update_data(photo_5=fifth_photo)
        await state.set_state(OrderCreating.sixth_photo)
        await message.answer('Фото добавлено - 5 из 6. Добавьте следующую...')


# Принимаем шестую фотографию заказа
@order_creating_router.message(content_types=['photo'], state=OrderCreating.sixth_photo)
async def take_fifth_photo(message: types.Message, state: FSMContext):
    if 'sixth_photo' not in await state.get_data():
        sixth_photo = message.photo[-1].file_id
        await state.update_data(photo_6=sixth_photo)
        await state.set_state(OrderCreating.price)
        await message.answer('Фото добавлено - 6 из 6.'
                             'Введите цену заказа...', reply_markup=remove_keyboard)


# Принимаем название заказа
@order_creating_router.message(state=OrderCreating.price)
async def take_price(message: types.Message, state: FSMContext):
    price = message.text

    if await price_is_valid(price, message):
        await state.update_data(price=price)
        await state.set_state(OrderCreating.address)
        await message.answer('Отправьте геопозицию заказа...', reply_markup=send_self_geoposition)


# Принимаем геопозицию заказа
@order_creating_router.message(state=OrderCreating.address, content_types=['location'])
async def take_geoposition(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await state.update_data(latitude=latitude, longitude=longitude)

    station_name, distance = find_nearest_underground((latitude, longitude))
    await state.update_data(underground=station_name, underground_distance=distance)

    await state.set_state(OrderCreating.time)
    await message.answer('Введите время исполнения заказа...', reply_markup=remove_keyboard)


# Принимаем время исполнения заказа
@order_creating_router.message(state=OrderCreating.time)
async def take_time(message: types.Message, state: FSMContext, bot: Bot, db: Database):
    time = message.text

    if await time_is_valid(time, message):
        await state.update_data(time=time, creator_id=message.from_user.id, status=1)
        data = await state.get_data()

        order = Order().load_from_data(data)
        text, photos = get_order_template(order)

        if len(photos) == 0:
            await message.answer(text)
        else:
            photos[0].caption = text
            await bot.send_media_group(message.chat.id, photos)

        await state.update_data(order=order)
        await state.set_state(OrderCreating.confirmation)
        await message.answer('Сохраняем заказ?', reply_markup=save_order_keyboard)


# Принимаем время исполнения заказа
@order_creating_router.message(state=OrderCreating.confirmation)
async def take_time(message: types.Message, state: FSMContext, db: Database):
    answer = message.text

    if answer == save_order_keyboard.keyboard[0][0].text:
        await (await state.get_data())['order'].save(db)
        await message.answer('Отлично! Заказ сохранен. '
                             'Вам осталось подождать, пока мы найдем для него исполнителя...')
        await main_menu(message, state)

    elif answer == save_order_keyboard.keyboard[1][0].text:
        await main_menu(message, state)

    else:
        await message.answer('Извините я вас не понимаю. Выберите варианты, предложенные мною...',
                             reply_markup=save_order_keyboard)


