# Обратная связь
from aiogram import types, Router

from tgbot.filters.main_menu import FeedbackFilter
from tgbot.keyboards.reply.reply import *

feedback_router = Router()


@feedback_router.message(FeedbackFilter())
async def start(message: types.Message):
    await message.answer('Хотите оставить отзыв? Написать жалобу? Уведомить об неисправности?\n\n'
                         'Пишите нашим админам, они оперативно ответят вам на любые обращения:\n\n'
                         '@czarkiruha\n\n'
                         # '@SNK_888\n'
                         # '@kohagu\n'
                         # '@KovalevaAnzhelika\n\n'
                         'Спасибо за обратную связь!', reply_markup=main_menu_keyboard)
