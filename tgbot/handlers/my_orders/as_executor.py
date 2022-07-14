from aiogram import types, Bot, Router, F
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.database.database import Database

from tgbot.keyboards.inline.my_orders import get_orders_list_keyboard, order_status_smile_dict, back_keyboard, \
    get_order_activity_keyboard_for_executor, MyOrdersCD

from tgbot.misc.states import MyOrders
from tgbot.misc.templates import get_order_template
from .scripts import check_back_to_role, delete_photo_messages, notify_creator_about_denial, \
    request_creator_about_completing

my_executor_orders_router = Router()


async def send_orders(user_id, message, db):
    orders = await db.get_orders_as_executor(user_id)
    if len(orders) == 0:
        message.edit_text('У вас нет ни одного заказа c ролью "работник".', reply_markup=back_keyboard)

    orders_list_keyboard = get_orders_list_keyboard(orders)
    await message.edit_text('Ваши заказы с ролью "работник":\n'
                            f'\t{order_status_smile_dict[2]} - в процессе выполнения\n'
                            f'\t{order_status_smile_dict[3]} - завершен\n', reply_markup=orders_list_keyboard)


@my_executor_orders_router.callback_query(MyOrdersCD.filter(F.states_group == 'my_orders'), state=MyOrders.orders_as_executor)
async def send_order(call: types.CallbackQuery, callback_data: MyOrdersCD, bot: Bot, state: FSMContext, db: Database):
    if await check_back_to_role(call, callback_data, state):
        order_id = callback_data.value
        order = await db.get_order_by_id(order_id)
        text, photos = get_order_template(order)
        reply_markup = get_order_activity_keyboard_for_executor(order)

        await bot.delete_message(call.message.chat.id, call.message.message_id)

        photo_messages = []
        if len(photos) != 0:
            photo_messages = await bot.send_media_group(chat_id=call.message.chat.id, media=photos)

        await state.set_state(MyOrders.order_as_executor)
        await state.update_data(photo_messages=photo_messages, order=order)
        await bot.send_message(call.from_user.id, text, reply_markup=reply_markup)


@my_executor_orders_router.callback_query(MyOrdersCD.filter(F.states_group == 'my_orders'), state=MyOrders.order_as_executor)
async def take_order_decision(call: types.CallbackQuery, callback_data: MyOrdersCD, bot: Bot, state: FSMContext, db: Database):
    data = await state.get_data()

    if callback_data.value == 'back':
        await delete_photo_messages(state, bot)
        await send_orders(call.from_user.id, call.message, db)
        await state.set_state(MyOrders.orders_as_executor)

    elif callback_data.value == 'complete':
        active_creator_requests = await db.get_active_request(data['order'].id, call.from_user.id, 'creator')
        active_executor_requests = await db.get_active_request(data['order'].id, call.from_user.id, 'executor')
        print(active_creator_requests, active_executor_requests)

        if len(active_creator_requests) != 0:
            order = data['order']
            await db.finish_request(active_creator_requests[0], True)
            await db.alter_order(order.id, status=3)
            await bot.send_message(order.creator_id,
                                   f'✅ Исполнитель заказа "{order.name}" подтвердил его завершение.')
            await bot.send_message(order.executor_id,
                                   f'✅ Заказ "{order.name}" был завершен.', reply_markup=back_keyboard)

        elif len(active_executor_requests) == 0:
            await request_creator_about_completing(data['order'], bot, db)
            await delete_photo_messages(state, bot)
            await call.message.edit_text('Заявка на заверешние заказа была отправлена заказчику.\t '
                                         'После его подтверждения заказ будет помечен, как  "заверешенный"',
                                         reply_markup=back_keyboard)

        else:
            await call.message.edit_text('У вас уже есть одна активная завяка на подтверждение данного заказа.',
                                         reply_markup=back_keyboard)

    elif callback_data.value == 'deny':
        await db.alter_order(order_id=data['order'].id, executor_id=None, status=1)
        await notify_creator_about_denial(data['order'], bot)
        await delete_photo_messages(state, bot)
        await send_orders(call.from_user.id, call.message, db)
        await state.set_state(MyOrders.orders_as_executor)
