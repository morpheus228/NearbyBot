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

