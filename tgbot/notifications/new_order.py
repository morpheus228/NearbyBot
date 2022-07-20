from aiogram import F, types, Bot

from tgbot.database.database import Database
from tgbot.handlers import notifications_router
from tgbot.keyboards.inline.inline import get_order_notification_keyboard, OrderNotificationCD
from tgbot.misc import replicas
from tgbot.misc.searching import find_users_for_mailing
from tgbot.misc.templates import get_order_template, get_user_template
from tgbot.validation.orders_count import check_orders_count_for_executor


async def notify_about_new_order(order, db: Database, bot):
    user_rows = await find_users_for_mailing(order, db)
    reply_markup = get_order_notification_keyboard(order)
    text, photos = get_order_template(order)
    text = '🆕 Мы нашли вам новый заказ!\n(Отменить уведомления можно в Настройках /settings)\n\n'+ text
    photo_messages = []

    for user_row in user_rows:
        local_text = text + f'\n<b>Расстояние до вас:</b> {round(user_row[1], 2)} км.'
        if len(photos) != 0:
            photo_messages = await bot.send_media_group(chat_id=user_row[0], media=photos)
        message = await bot.send_message(user_row[0], local_text, reply_markup=reply_markup)

        await db.add_notification(message.message_id, order.id)
        for photo_message in photo_messages:
            await db.add_related_message(photo_message.message_id, message.message_id)


async def delete_related_messages(message, bot, db):
    message_ids = await db.get_related_messages(message.message_id)
    await db.delete_related_messages(message.message_id)

    for message_id in message_ids:
        await bot.delete_message(chat_id=message.chat.id, message_id=message_id)


@notifications_router.callback_query(OrderNotificationCD.filter(F.states_group == 'order_notification'))
async def take_decision_about_new_order(call: types.CallbackQuery, callback_data: OrderNotificationCD, db: Database, bot: Bot):
    message_id = call.message.message_id
    notification = await db.get_notification(message_id)
    await delete_related_messages(call.message, bot, db)

    if callback_data.value == 'disaccept':
        await db.finish_notification(message_id, False)
        await call.message.delete()

    elif callback_data.value == 'accept':
        if not await check_orders_count_for_executor(call.from_user.id, db):
            await call.message.edit_text(replicas.warnings.orders_limit_for_executor)

        else:
            await db.finish_notification(message_id, True)
            order = await db.get_order_by_id(notification.order_id)

            if await db.check_order_availability(order.id):
                await call.message.edit_reply_markup(reply_markup=None)
                await db.alter_order(order.id, status=2, executor_id=call.from_user.id)

                executor_profile = await db.get_user_profile_by_id(call.from_user.id)
                creator_profile = await db.get_user_profile_by_id(order.creator_id)

                await call.message.answer(get_user_template(creator_profile, 'creator'))
                await bot.send_message(order.creator_id, get_user_template(executor_profile, 'executor', order.name))

            else:
                await call.message.edit_text(f'Извиняемся! Данный заказ уже взял другой исполнитель.')
