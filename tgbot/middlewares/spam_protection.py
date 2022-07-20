from time import time
from aiogram import BaseMiddleware


from tgbot.keyboards.reply.reply import main_menu_keyboard
from tgbot.config import PAUSE_TIME, IGNORE_TIME, WARNINGS_LIMIT


class AntiSpamMiddleware(BaseMiddleware):
    WARNING_TEXT = 'Слишком частые одинаковые запросы! За спам вы будете заблокированы!'
    IGNORE_TEXT = f'Ваш доступ к данному хендлеру заблокирован на {round(IGNORE_TIME / 60, 1)} минуты!'

    def __init__(self, dp):

        self.dp = dp
        self.commands = list(dp['commands'].keys())

        self.text_commands = []
        for line in main_menu_keyboard.keyboard:
            for elem in line:
                self.text_commands.append(elem.text)

        self.last_calls = {}
        self.warnings_counters = {}
        self.ignore_times = {}

    async def __call__(self, handler, event, data):
        if event.text not in self.text_commands + self.commands:
            return await handler(event, data)

        else:
            user_id = event.from_user.id
            last_call = self.last_calls.get(user_id, 0)
            self.last_calls[user_id] = time()

            if user_id in self.ignore_times.keys():
                if time() - self.ignore_times[user_id] >= IGNORE_TIME:
                    self.ignore_times.pop(user_id)
                    return await handler(event, data)

            elif user_id in self.warnings_counters.keys():

                if time() - last_call < PAUSE_TIME:
                    self.warnings_counters[user_id] += 1

                    if self.warnings_counters[user_id] >= WARNINGS_LIMIT:
                        self.ignore_times[user_id] = time()
                        self.warnings_counters.pop(user_id)
                        await event.answer(self.IGNORE_TEXT)

                    else:
                        await event.answer(self.WARNING_TEXT)

                else:
                    self.warnings_counters.pop(user_id)
                    return await handler(event, data)

            else:
                if time() - last_call < PAUSE_TIME:
                    self.warnings_counters[user_id] = 1
                    await event.answer(self.WARNING_TEXT)

                else:
                    return await handler(event, data)