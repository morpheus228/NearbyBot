from tgbot.database.schemas import User
import re

phone_number_rule = re.compile('^((\+?7|8)[ \-] ?)?((\(\d{3}\))|(\d{3}))?([ \-])?(\d{3}[\- ]?\d{2}[\- ]?\d{2})$')


async def name_is_valid(name, message):
    if len(name) > User.name_length_limit:
        await message.answer(f'Имя не может быть длиннее, чем {User.name_length_limit} символов. '
                             f'Введите свое имя заново...')
        return False
    return True


async def age_is_valid(age, message):
    if age.isdigit():
        if int(age) <= User.age_limit:
            return True

    await message.answer(f'Возраст должен состоять из цифр и быть меньше {User.age_limit} лет. '
                         f'Введите свой возраст заново...')
    return False


async def description_is_valid(description, message):
    if len(description) > User.description_length_limit:
        await message.answer(f'Ваше описание не может быть длиннее, чем {User.description_length_limit} символов. '
                             f'Напишите пару слов о себе заново...')
        return False
    return True


async def phone_number_is_valid(phone_number, message):
    if phone_number is None:
        return True
    else:
        if not phone_number_rule.search(phone_number):
            await message.answer(f'Номер введён неправильно. '
                                 f'Введите свой номер телефона заново...')
            return False
        else:
            return True
