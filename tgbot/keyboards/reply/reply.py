from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

remove_keyboard = ReplyKeyboardRemove()

without_number_phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='🚫 Без номера телефона')]],
    resize_keyboard=True, one_time_keyboard=True)

without_description_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='🚫 Без подробного описания')]],
    resize_keyboard=True, one_time_keyboard=True)

without_photo_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='🚫 Без фотографий')]],
    resize_keyboard=True, one_time_keyboard=True)

stop_photo_adding_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Предыдущих фотогорафий хватит')]],
    resize_keyboard=True, one_time_keyboard=True)

send_self_geoposition = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отправить свою геопозицию', request_location=True)]],
    resize_keyboard=True, one_time_keyboard=True)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Создать заказ'), KeyboardButton(text='Найти заказ')],
        [KeyboardButton(text='Мои заказы'), KeyboardButton(text='Мой профиль')],
        [KeyboardButton(text='Обратная связь')],
    ],
    resize_keyboard=True, one_time_keyboard=True)

save_order_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да! Все верно')],
        [KeyboardButton(text='Нет! Отмена')]
    ],
    resize_keyboard=True, one_time_keyboard=True)
