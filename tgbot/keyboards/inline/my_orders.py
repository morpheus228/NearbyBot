from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

order_status_smile_dict = {
    1: '🆓',
    2: '♻',
    3: '✅'
}


class MyOrdersCD(CallbackData, prefix=''):
    value: str
    states_group: str = 'my_orders'


order_role_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='🧑‍💼 Заказчик',
                              callback_data=MyOrdersCD(value='creator').pack()),
         InlineKeyboardButton(text='🛠 Исполнитель',
                              callback_data=MyOrdersCD(value='executor').pack()),
         ],
        [InlineKeyboardButton(text='🔙 НАЗАД 🔙',
                              callback_data=MyOrdersCD(value='back').pack())],
    ]).as_markup()


back_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='🔙 НАЗАД 🔙',
                              callback_data=MyOrdersCD(value='back').pack())],
    ]).as_markup()


def get_orders_list_keyboard(orders):
    orders_list_keyboard = InlineKeyboardBuilder()
    for order in orders:
        smile = order_status_smile_dict[order.status]
        orders_list_keyboard.row(InlineKeyboardButton(text=f'{smile} {order.name}',
                                                      callback_data=MyOrdersCD(value=order.id).pack()))

    orders_list_keyboard.row(InlineKeyboardButton(text='🔙 НАЗАД 🔙',
                                                  callback_data=MyOrdersCD(value='back').pack()))
    return orders_list_keyboard.as_markup()


def get_order_activity_keyboard_for_creator(order):
    order_activity_keyboard_for_creator = InlineKeyboardBuilder()

    if order.status == 1:
        order_activity_keyboard_for_creator.row(InlineKeyboardButton(text='❌ Удалить',
                                                                     callback_data=MyOrdersCD(value='delete').pack()))

    elif order.status == 2:
        order_activity_keyboard_for_creator.row(InlineKeyboardButton(text='❌ Удалить',
                                                                     callback_data=MyOrdersCD(value='delete').pack()))
        order_activity_keyboard_for_creator.row(InlineKeyboardButton(text='🚫 Отказаться от исполнителя',
                                                                     callback_data=MyOrdersCD(value='deny').pack()))
        order_activity_keyboard_for_creator.row(InlineKeyboardButton(text='✅ Завершить',
                                                                     callback_data=MyOrdersCD(value='complete').pack()))

    order_activity_keyboard_for_creator.row(InlineKeyboardButton(text='🔙 Назад',
                                                                 callback_data=MyOrdersCD(value='back').pack()))
    return order_activity_keyboard_for_creator.as_markup()


def get_order_activity_keyboard_for_executor(order):
    order_activity_keyboard_for_executor = InlineKeyboardBuilder()

    if order.status == 2:
        order_activity_keyboard_for_executor.row(InlineKeyboardButton(text='🚫 Отказаться от заказа',
                                                                     callback_data=MyOrdersCD(value='deny').pack()))
        order_activity_keyboard_for_executor.row(InlineKeyboardButton(text='✅ Завершить',
                                                                     callback_data=MyOrdersCD(value='complete').pack()))

    order_activity_keyboard_for_executor.row(InlineKeyboardButton(text='🔙 Назад',
                                                                  callback_data=MyOrdersCD(value='back').pack()))
    return order_activity_keyboard_for_executor.as_markup()