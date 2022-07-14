from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.misc.states import OrderCreating
from tgbot.keyboards.reply.reply import without_photo_keyboard, stop_photo_adding_keyboard


class WithoutPhotoFilter(BaseFilter):
    text_messages = [without_photo_keyboard.keyboard[0][0].text,
                     stop_photo_adding_keyboard.keyboard[0][0].text]

    states = [OrderCreating.first_photo.state,
              OrderCreating.second_photo.state,
              OrderCreating.third_photo.state,
              OrderCreating.fourth_photo.state,
              OrderCreating.fifth_photo.state,
              OrderCreating.sixth_photo.state]

    async def __call__(self, message: Message, state: FSMContext):
        state = await state.get_state()
        return (message.text in self.text_messages) and (state in self.states)