from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message
from tgbot.keyboards.reply.reply import main_menu_keyboard


class NewOrderFilter(BaseFilter):
    command = '/new_order'
    text_message = main_menu_keyboard.keyboard[0][0].text

    async def __call__(self, message: Message):
        return message.text in [self.command, self.text_message]


class FindOrderFilter(BaseFilter):
    command = '/find_order'
    text_message = main_menu_keyboard.keyboard[0][1].text

    async def __call__(self, message: Message):
        return message.text in [self.command, self.text_message]


class MyOrdersFilter(BaseFilter):
    command = '/my_orders'
    text_message = main_menu_keyboard.keyboard[1][0].text

    async def __call__(self, message: Message):
        return message.text in [self.command, self.text_message]


class MyProfileFilter(BaseFilter):
    command = '/my_profile'
    text_message = main_menu_keyboard.keyboard[1][1].text

    async def __call__(self, message: Message):
        return message.text in [self.command, self.text_message]


class FeedbackFilter(BaseFilter):
    command = '/feedback'
    text_message = main_menu_keyboard.keyboard[2][0].text

    async def __call__(self, message: Message):
        return message.text in [self.command, self.text_message]


class SettingsFilter(BaseFilter):
    command = '/settings'
    text_message = main_menu_keyboard.keyboard[2][1].text

    async def __call__(self, message: Message):
        return message.text in [self.command, self.text_message]