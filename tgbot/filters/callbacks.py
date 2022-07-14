from typing import Any

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext
from tgbot.keyboards.inline.my_orders import MyOrdersCD
from tgbot.misc.states import MyOrders


def prefix(string):
    return string.split(':')[0]


class MyOrdersStateFilter(BaseFilter):
    st: str

    async def __call__(self, call: CallbackQuery, state: FSMContext):
        pass
        # callback_data =
        # cond1 = (await state.get_state()) == self.state
        # cond2 = prefix(call.data) == 'my_orders'
        # return (await state.get_state() == self.state) and (callback_data.state == 'role')
