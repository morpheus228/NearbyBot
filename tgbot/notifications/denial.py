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
