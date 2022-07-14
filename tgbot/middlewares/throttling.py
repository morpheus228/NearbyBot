from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags.getter import get_flag
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        "spin": TTLCache(maxsize=10_000, ttl=1),
        "default": TTLCache(maxsize=10_000, ttl=1)
    }

    async def __call__(self, handler, event, data):
        throttling_key = get_flag(data, "throttling_key")
        print(throttling_key)
        print(self.caches)

        if throttling_key is not None and throttling_key in self.caches:
            if event.chat.id in self.caches[throttling_key]:
                return
            else:
                self.caches[throttling_key][event.chat.id] = None
        return await handler(event, data)