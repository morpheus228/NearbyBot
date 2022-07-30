# Обратная связь
from aiogram import types, Router

from tgbot.filters.main_menu import FeedbackFilter
from tgbot.handlers import commands_router
from tgbot.keyboards.reply.reply import *

feedback_router = Router()


@commands_router.message(FeedbackFilter())
async def start(message: types.Message):
    await message.answer('Хотите оставить отзыв? Написать жалобу? Уведомить об неисправности?\n\n'
                         'Напишите в нашу техподдержку, модераторы оперативно ответят на любые ваши обращения:\n\n'
                         '@nearby_support\n\n'
                         'Спасибо за обратную связь!', reply_markup=main_menu_keyboard)
