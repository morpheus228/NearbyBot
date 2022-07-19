from aiogram import BaseMiddleware


class AllMessageHandlersMiddleware(BaseMiddleware):
    def __init__(self, dp):
        self.db = dp['db']

    async def __call__(self, handler, event, data):
        result = await handler(event, data)
        await self.db.add_message_event(event)
        return result


class AllCallbackHandlersMiddleware(BaseMiddleware):
    def __init__(self, dp):
        self.db = dp['db']

    async def __call__(self, handler, event, data):
        result = await handler(event, data)
        await self.db.add_callback_event(event)
        return result
