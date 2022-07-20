from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyProfileCD(CallbackData, prefix=''):
    value: str
    states_group: str = 'my_profile'


my_profile_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='Имя',
                              callback_data=MyProfileCD(value='name').pack()),
         InlineKeyboardButton(text='Номер телефона',
                              callback_data=MyProfileCD(value='phone_number').pack())],

        [InlineKeyboardButton(text='Описание',
                              callback_data=MyProfileCD(value='description').pack()),
         InlineKeyboardButton(text='Возраст',
                              callback_data=MyProfileCD(value='age').pack())],

        [InlineKeyboardButton(text='Заполнить профиль заново',
                              callback_data=MyProfileCD(value='full').pack())],

        [InlineKeyboardButton(text='🔙 НАЗАД 🔙',
                              callback_data=MyProfileCD(value='back').pack())],
    ]).as_markup()