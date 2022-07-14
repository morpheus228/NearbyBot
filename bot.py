import asyncio
import logging

from aiogram import Bot, Dispatcher, types
# from aiogram.dispatcher.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
# from tgbot.filters.admin import AdminFilter

from tgbot.handlers.feedback import feedback_router
from tgbot.handlers.find_order import find_order_router
from tgbot.handlers.my_orders.as_creator import my_creator_orders_router
from tgbot.handlers.my_orders.as_executor import my_executor_orders_router
from tgbot.handlers.my_orders.router import my_orders_router
from tgbot.handlers.my_profile import my_profile_router
from tgbot.handlers.user_registration import user_registration_router
from tgbot.handlers.order_creating import order_creating_router

from tgbot.database.database import Database
from tgbot.middlewares.spam_protection import AntiSpamMiddleware

from tgbot.middlewares.user_activity import *

logger = logging.getLogger(__name__)


async def register_default_commands(bot):
    await bot.set_my_commands([
        types.BotCommand(command='find_order', description="Найти заказ"),
        types.BotCommand(command="my_orders", description="Мои заказы"),
        types.BotCommand(command="my_profile", description="Мой профиль"),
        types.BotCommand(command="new_order", description="Создать заказ"),
        types.BotCommand(command="feedback", description="Техподдержка"),
    ])


async def register_all_middlewares(dp):
    dp.callback_query.middleware(AllCallbackHandlersMiddleware(dp))
    dp.message.middleware(AllMessageHandlersMiddleware(dp))

    commands = await dp['bot'].get_my_commands()
    dp.message.middleware(AntiSpamMiddleware(dp, commands))


def register_all_handlers(dp):
    for router in [
        my_profile_router,
        user_registration_router,
        order_creating_router,
        find_order_router,
        my_executor_orders_router,
        my_creator_orders_router,
        my_orders_router,
        feedback_router
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

    await register_default_commands(bot)
    await register_all_middlewares(dp)
    await db.connect(config.db)

    register_all_handlers(dp)

    # Start
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
