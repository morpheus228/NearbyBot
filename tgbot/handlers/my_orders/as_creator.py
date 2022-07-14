from aiogram import types, Bot, Router, F
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.database.database import Database

from tgbot.keyboards.inline.my_orders import back_keyboard, get_orders_list_keyboard, order_status_smile_dict, \
    get_order_activity_keyboard_for_creator, MyOrdersCD

from tgbot.misc.states import MyOrders
from tgbot.misc.templates import get_order_template
from .scripts import check_back_to_role, delete_photo_messages, notify_executor_about_denial, \
    request_executor_about_completing

my_creator_orders_router = Router()


async def send_orders(user_id, message, db):
    orders = await db.get_orders_as_creator(user_id)
    if len(orders) == 0:
        message.edit_text('У вас нет ни одного заказа c ролью "заказчик".', reply_markup=back_keyboard)

    orders_list_keyboard = get_orders_list_keyboard(orders)
    await message.edit_text('Ваши заказы c ролью "заказчик":\n'
                            f'\t{order_status_smile_dict[1]} - в поисках работника\n'
                            f'\t{order_status_smile_dict[2]} - в процессе выполнения\n',
                            reply_markup=orders_list_keyboard)


@my_creator_orders_router.callback_query(MyOrdersCD.filter(F.states_group == 'my_orders'), state=MyOrders.orders_as_creator)
async def send_order(call: types.CallbackQuery, callback_data: MyOrdersCD, bot: Bot, state: FSMContext, db: Database):
    if await check_back_to_role(call, callback_data, state):
        order_id = callback_data.value
        order = await db.get_order_by_id(order_id)
        text, photos = get_order_template(order)
        reply_markup = get_order_activity_keyboard_for_creator(order)

        await bot.delete_message(call.message.chat.id, call.message.message_id)

        photo_messages = []
        if len(photos) != 0:
            photo_messages = await bot.send_media_group(chat_id=call.message.chat.id, media=photos)

        await state.set_state(MyOrders.order_as_creator)
        await state.update_data(photo_messages=photo_messages, order=order)
        await bot.send_message(call.from_user.id, text, reply_markup=reply_markup)


@my_creator_orders_router.callback_query(MyOrdersCD.filter(F.states_group == 'my_orders'), state=MyOrders.order_as_creator)
async def take_order_decision(call: types.CallbackQuery, callback_data: MyOrdersCD, bot: Bot, state: FSMContext, db: Database):
    data = await state.get_data()

    if callback_data.value == 'back':
        await delete_photo_messages(state, bot)
        await send_orders(call.from_user.id, call.message, db)
        await state.set_state(MyOrders.orders_as_creator)

    elif callback_data.value == 'delete':
        await db.delete_order(data['order'].id)
        await delete_photo_messages(state, bot)
        await send_orders(call.from_user.id, call.message, db)
        await state.set_state(MyOrders.orders_as_creator)
        if data['order'].executor_id is not None:
            await notify_executor_about_denial(data['order'], bot)

    elif callback_data.value == 'complete':
        active_creator_requests = await db.get_active_request(data['order'].id, call.from_user.id, 'creator')
        active_executor_requests = await db.get_active_request(data['order'].id, call.from_user.id, 'executor')

        if len(active_executor_requests) != 0:
            order = data['order']
            await db.finish_request(active_executor_requests[0], True)
            await db.alter_order(order.id, status=3)
            await call.message.edit_text(f'✅ Заказ "{order.name}" был завершен.', reply_markup=back_keyboard)
            await bot.send_message(order.executor_id,
                                   f'✅ Заказчик заказа "{order.name}" подтвердил его завершение.')

        if len(active_creator_requests) == 0:
            await request_executor_about_completing(data['order'], bot, db)
            await delete_photo_messages(state, bot)
            await state.update_data(user_id=call.from_user.id)
            await call.message.edit_text('Заявка на заверешние заказа была отправлена работнику.\t '
                                         'После его подтверждения заказ будет помечен, как  "заверешенный"',
                                         reply_markup=back_keyboard)
        else:
            await call.message.edit_text('У вас уже есть одна активная завяка на подтверждение данного заказа.',
                                         reply_markup=back_keyboard)

    elif callback_data.value == 'deny':
        await db.alter_order(order_id=data['order'].id, executor_id=None, status=1)
        await notify_executor_about_denial(data['order'], bot)
        await delete_photo_messages(state, bot)
        await send_orders(call.from_user.id, call.message, db)
        await state.set_state(MyOrders.orders_as_executor)






