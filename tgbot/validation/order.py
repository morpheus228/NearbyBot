from tgbot.database.schemas import Order


async def name_is_valid(name, message):
    if len(name) > Order.name_length_limit:
        await message.answer(f'Название не может быть длиннее, чем {Order.name_length_limit} символов. '
                             f'Введите название заказа заново...')
        return False
    return True


async def description_is_valid(description, message):
    if description is None:
        return True
    else:
        if len(description) > Order.description_length_limit:
            await message.answer(f'Подробное описание не может быть длиннее, чем {Order.description_length_limit} символов. '
                                 f'Введите подробное описание заказа заново...')
            return False
        return True


async def price_is_valid(price, message):
    if not price.isdigit():
        await message.answer(f'Цена должна состоять из цифр.\n'
                             f'Введите цену заказа заново...')
        return False

    elif int(price) > Order.price_limit:
        await message.answer(f'Цена дожна быть меньше, чем {Order.price_limit}.\n'
                             f'Введите цену заказа заново...')
        return False

    return True


async def time_is_valid(time, message):
    if time is None:
        return True
    else:
        parts = list(time.split(':'))
        if (len(parts) == 2) and (check_hours(parts[0])) and (check_minutes(parts[1])):
            return True
        else:
            await message.answer(f'Время не соответсвует формату "12:00". Попробуйте снова...')
            return False


def check_hours(string):
    if string.isdigit():
        if int(string) <= 24:
            return True
    return False


def check_minutes(string):
    if string.isdigit():
        if int(string) <= 60:
            return True
    return False