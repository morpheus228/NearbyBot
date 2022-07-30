from aiogram import BaseMiddleware
from tgbot.handlers import user_registration


class RegistrationCheck(BaseMiddleware):
    def __init__(self, dp):
        self.db = dp['db']
        self.commands = list(dp['commands'].keys())

    async def __call__(self, handler, event, data):
        if event.text in self.commands:

            if await self.db.is_user_registered(event.from_user.id) or event.text == '/start':
                return await handler(event, data)
            else:
                await event.answer('Вы не завершили регистрацию!')
                return await user_registration.start(event, data['state'], data['db'])

        return await handler(event, data)