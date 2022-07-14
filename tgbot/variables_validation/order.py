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
    if price.isdigit():
        if int(price) <= Order.price_limit:
            return True

    await message.answer(f'Цена должна состоять из цифр и быть меньше, чем {Order.price_limit}. '
                         f'Введите цену заказа заново...')
    return False


async def time_is_valid(time, message):
    if len(time) > Order.time_length_limit:
        await message.answer(f'Время не может быть длиннее, чем {Order.time_length_limit} символов. '
                             f'Введите время выполнения заказа заново...')
        return False
    return True
