import asyncio
import logging

from aiogram import Bot, Dispatcher, types
# from aiogram.dispatcher.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.handlers import commands_router, notifications_router
from tgbot.handlers.feedback import feedback_router

from tgbot.handlers.find_order import find_order_router
from tgbot.handlers.my_orders.as_creator import my_creator_orders_router
from tgbot.handlers.my_orders.as_executor import my_executor_orders_router
from tgbot.handlers.my_orders.router import my_orders_router
from tgbot.handlers.my_profile import my_profile_router
from tgbot.handlers.settings import settings_router
from tgbot.handlers.user_registration import user_registration_router
from tgbot.handlers.order_creating import order_creating_router

from tgbot.database.database import Database
from tgbot.middlewares.registration import RegistrationCheck
from tgbot.middlewares.spam_protection import AntiSpamMiddleware

from tgbot.middlewares.user_activity import *

logger = logging.getLogger(__name__)


async def register_default_commands(dp):
    command_list = []
    for key in dp['commands']:
        command_list.append(types.BotCommand(command=key[1:], description=dp['commands'][key]))

    await dp['bot'].set_my_commands(command_list)


def register_all_middlewares(dp):
    dp.callback_query.middleware(AllCallbackHandlersMiddleware(dp))
    dp.message.middleware(AllMessageHandlersMiddleware(dp))
    dp.message.middleware(AntiSpamMiddleware(dp))
    dp.message.middleware(RegistrationCheck(dp))


def register_all_handlers(dp):
    for router in [
        commands_router,
        notifications_router,
        my_orders_router,
        my_executor_orders_router,
        my_creator_orders_router,
        feedback_router,
        settings_router,
        find_order_router,
        my_profile_router,
        user_registration_router,
        order_creating_router,
    ]:
        dp.include_router(router)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    db = Database()

    dp['config'] = config
    dp['db'] = db
    dp['bot'] = bot

    dp['commands'] = {'/find_order': "Найти заказ",
                      "/new_order": "Создать заказ",
                      "/my_orders": "Мои заказы",
                      "/my_profile": "Мой профиль",
                      "/settings": "Настройки",
                      "/feedback": "Техподдержка"}

    await register_default_commands(dp)
    await db.connect(config.db)
    register_all_middlewares(dp)
    register_all_handlers(dp)

    # Start
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
