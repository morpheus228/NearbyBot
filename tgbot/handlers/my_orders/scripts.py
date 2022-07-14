from tgbot.keyboards.inline.inline import get_confirmation_of_completing_order_keyboard
from tgbot.keyboards.inline.my_orders import order_role_keyboard
from tgbot.misc.states import MyOrders


async def check_back_to_role(call, callback_data, state):
    if callback_data.value == 'back':
        await call.message.edit_text('Выберите вашу роль в заказах...', reply_markup=order_role_keyboard)
        await state.set_state(MyOrders.role)
        return False
    else:
        return True


async def delete_photo_messages(state, bot):
    data = await state.get_data()
    await state.update_data(photo_messages=[])
    for photo_message in data['photo_messages']:
        await bot.delete_message(chat_id=photo_message.chat.id, message_id=photo_message.message_id)


async def notify_executor_about_denial(order, bot):
    executor_id = order.executor_id
    await bot.send_message(executor_id, f'К сожалению, заказчик заказа "{order.name}" '
                                        f'отказался от вашего исполнения или удалил свой заказ.\n'
                                        f'Приносим свои извинения!')


async def notify_creator_about_denial(order, bot):
    creator_id = order.creator_id
    await bot.send_message(creator_id, f'К сожалению, исполнитель заказа "{order.name}" отказался от него.\n'
                                       f'Данный заказ снова доступен для других иполнителей.\n'
                                       f'Приносим свои извинения!')


async def request_executor_about_completing(order, bot, db):
    executor_id = order.executor_id
    reply_markup = get_confirmation_of_completing_order_keyboard(order.id, 'creator')
    message = await bot.send_message(executor_id, reply_markup=reply_markup,
                        text=f'Заказчик заказа "{order.name}" запрашивает у вас подтверждение о завершении заказа...')
    await db.add_request(order=order, message_id=message.message_id, requester='creator')


async def request_creator_about_completing(order, bot, db):
    creator_id = order.creator_id
    reply_markup = get_confirmation_of_completing_order_keyboard(order.id, 'executor')
    message = await bot.send_message(creator_id, reply_markup=reply_markup,
                    text=f'Исполнитель заказа "{order.name}" запрашивает у вас подтверждение о завершении заказа...')
    await db.add_request(order=order, message_id=message.message_id, requester='executor')

