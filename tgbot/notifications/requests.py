from tgbot.keyboards.inline.inline import get_confirmation_of_completing_order_keyboard


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