from tgbot.keyboards.reply.reply import main_menu_keyboard


async def main_menu(message, state):
    await state.clear()
    await message.answer('Главное меню:', reply_markup=main_menu_keyboard)
