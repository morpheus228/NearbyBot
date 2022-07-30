from tgbot.database.schemas import User
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

from tgbot.keyboards.reply.reply import notifications_decision_keyboard


async def name_is_valid(name, message):
    if len(name) > User.name_length_limit:
        await message.answer(f'Имя не может быть длиннее, чем {User.name_length_limit} символов. '
                             f'Введите свое имя заново...')
        return False
    return True


async def age_is_valid(age, message):
    if not age.isdigit():
        await message.answer(f'Возраст должен состоять из цифр.\n'
                             f'Введите свой возраст заново...')
        return False

    elif int(age) > User.age_limit:
        await message.answer(f'Возраст должен быть меньше {User.age_limit} лет.\n'
                             f'Введите свой возраст заново...')
        return False

    return True


async def description_is_valid(description, message):
    if description is None:
        return True
    else:
        if len(description) > User.description_length_limit:
            await message.answer(f'Ваше описание не может быть длиннее, чем {User.description_length_limit} символов. '
                                 f'Напишите пару слов о себе заново...')
            return False
        return True


async def phone_number_is_valid(phone_number, message):
    if phone_number is None:
        return True
    else:
        try:
            if (carrier._is_mobile(number_type(phonenumbers.parse(phone_number)))):
                return True
            else:
                await message.answer(f'Номер телефон введён неправильно. \n'
                                     f'(он должен соотвествовать формату +7 999 999 99 99) \n'
                                     f'Введите свой номер телефона заново...')
                return False
        except:
            await message.answer(f'Номер телефон введён неправильно. \n'
                                     f'(он должен соотвествовать формату +7 999 999 99 99) \n'
                                     f'Введите свой номер телефона заново...')
            return False


async def notifications_decision_is_valid(decision, message):
    if (decision == notifications_decision_keyboard.keyboard[0][0].text) or (decision == notifications_decision_keyboard.keyboard[0][1].text):
        return True
    else:
        await message.answer('Извините я вас не понимаю. Выберите варианты, предложенные мною.\n'
                             'Включить уведомления о новых заказах?')
        return False