from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext
from tgbot.keyboards.inline.my_orders import MyOrdersCD
from tgbot.misc.states import MyOrders


class RoleFilter(BaseFilter):
    async def __call__(self, callback_data: MyOrdersCD, state: FSMContext):
        return (await state.get_state() == MyOrders.role.state) and (callback_data.state == 'role')
