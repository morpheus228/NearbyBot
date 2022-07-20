from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SettingsCD(CallbackData, prefix=''):
    value: str
    states_group: str = 'settings'


notifications_true_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='📴 Выключить уведомления',
                              callback_data=SettingsCD(value='off').pack())],
        [InlineKeyboardButton(text='🆙 Обновить геопозицию',
                          callback_data=SettingsCD(value='update').pack())],
        [InlineKeyboardButton(text='🔙 НАЗАД 🔙',
                              callback_data=SettingsCD(value='back').pack())],
    ]).as_markup()


notifications_false_keyboard = InlineKeyboardBuilder([
        [InlineKeyboardButton(text='✅ Включить уведомления',
                              callback_data=SettingsCD(value='on').pack())],
        [InlineKeyboardButton(text='🔙 НАЗАД 🔙',
                          callback_data=SettingsCD(value='back').pack())],
    ]).as_markup()