from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class FindOrderCD(CallbackData, prefix=''):
    value: str
    states_group: str = 'find_order'


def get_order_keyboard(order):
    url = f'http://maps.yandex.com/?pt= {order.longitude}, {order.latitude} &z=16&l=map'

    order_keyboard = InlineKeyboardBuilder([
        # [InlineKeyboardButton(text='🗺 Пожаловаться',
        #                       callback_data=FindOrderCD(value='complaint').pack())],
        [InlineKeyboardButton(text='🗺 Посмотреть местоположение',
                              callback_data=FindOrderCD(value='map').pack(), url=url)],
        [InlineKeyboardButton(text='❌ Пропустить заказ',
                              callback_data=FindOrderCD(value='skip').pack())],
        [InlineKeyboardButton(text='✔ Принять заказ ',
                              callback_data=FindOrderCD(value='accept').pack())],
    ])

    return order_keyboard.as_markup()


class OrderNotificationCD(CallbackData, prefix=''):
    value: str
    states_group: str = 'order_notification'


def get_order_notification_keyboard(order):
    url = f'http://maps.yandex.com/?pt= {order.longitude}, {order.latitude} &z=16&l=map'

    order_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='🗺 Посмотреть местоположение',
                              callback_data=OrderNotificationCD(value='map').pack(), url=url)],
        [InlineKeyboardButton(text='❌ Отклонить заказ',
                              callback_data=OrderNotificationCD(value='disaccept').pack())],
        [InlineKeyboardButton(text='✔ Принять заказ ',
                              callback_data=OrderNotificationCD(value='accept').pack())],
    ])

    return order_keyboard.as_markup()


continue_order_finding_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='▶ Продолжить поиск заказов',
                              callback_data=FindOrderCD(value='skip').pack())],
    ]).as_markup()


class ConfirmationCD(CallbackData, prefix=''):
    order_id: int
    requester: str
    value: str
    states_group: str = 'confirmation'


def get_confirmation_of_completing_order_keyboard(order_id, requester):
    confirmation_of_completing_order_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='✔ Подтвердить ',
                        callback_data=ConfirmationCD(order_id=order_id, requester=requester, value='agree').pack())],
        [InlineKeyboardButton(text='❌ Отклонить',
                        callback_data=ConfirmationCD(order_id=order_id, requester=requester, value='disagree').pack())],
        ])
    return confirmation_of_completing_order_keyboard.as_markup()