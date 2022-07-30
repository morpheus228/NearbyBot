# Процесс создания нового заказа

from aiogram import types, Router, Bot, F
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.database.database import Database
from tgbot.filters.main_menu import MyOrdersFilter
from tgbot.keyboards.inline.my_orders import order_role_keyboard, MyOrdersCD
from tgbot.misc.states import MyOrders

from . import as_executor, as_creator
from .. import commands_router, notifications_router
from ...filters.callbacks import MyOrdersStateFilter
from ...keyboards.inline.inline import ConfirmationCD
from ...keyboards.reply.reply import main_menu_keyboard
from ...misc import replicas
from ...misc.main_router import main_menu

my_orders_router = Router()
my_orders_router.callback_query.bind_filter(MyOrdersStateFilter)


@commands_router.message(MyOrdersFilter())
async def start(message: types.Message, state: FSMContext):
    await message.answer('Выберите вашу роль в заказах...', reply_markup=order_role_keyboard)
    await state.set_state(MyOrders.role)


# @my_orders_router.callback_query(st=MyOrders.role.state)
@my_orders_router.callback_query(MyOrdersCD.filter(F.states_group == 'my_orders'), state=MyOrders.role)
async def take_order_role(call: types.CallbackQuery, callback_data: MyOrdersCD, state: FSMContext, db: Database):
    if callback_data.value == 'executor':
        await as_executor.send_orders(call.from_user.id, call.message, db)
        await state.set_state(MyOrders.orders_as_executor)

    elif callback_data.value == 'creator':
        await as_creator.send_orders(call.from_user.id, call.message, db)
        await state.set_state(MyOrders.orders_as_creator)

    elif callback_data.value == 'back':
        await call.message.delete()
        await main_menu(call.message, state)


@notifications_router.callback_query(ConfirmationCD.filter(F.states_group == 'confirmation'))
async def take_confirmation_of_completing(call: types.CallbackQuery, callback_data: ConfirmationCD, db: Database, bot: Bot):
    message_id = call.message.message_id
    request = await db.get_request_by_message_id(message_id)

    await bot.delete_message(call.message.chat.id, message_id)

    if request.agreement is None:

        order = await db.get_order_by_id(callback_data.order_id)

        if callback_data.value == 'agree':

            if callback_data.requester == 'executor':
                await bot.send_message(order.executor_id,
                                       f'✅ Заказчик заказа "{order.name}" подтвердил его завершение.')

            elif callback_data.requester == 'creator':
                await bot.send_message(order.creator_id,
                                       f'✅ Исполнитель заказа "{order.name}" подтвердил его завершение.')

            await db.finish_request(message_id, True)
            await db.alter_order(order.id, status=3)

        elif callback_data.value == 'disagree':

            if callback_data.requester == 'executor':
                await bot.send_message(order.executor_id,
                                       f'❌ Заказчик заказа "{order.name}" отклонил его завершение.')

            elif callback_data.requester == 'creator':
                await bot.send_message(order.creator_id,
                                       f'❌ Исполнитель заказа "{order.name}" отклонил его завершение.')

            await db.finish_request(message_id, False)
