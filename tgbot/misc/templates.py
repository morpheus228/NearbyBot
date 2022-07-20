from aiogram.types import InputMediaPhoto


def get_order_template(order):
    text = ''
    text += f'<b>{order.name}</b>\n'

    if order.description is not None:
        text += f'{order.description}\n\n'

    text += f'<b>Цена:</b> {order.price} руб.\n'

    if order.time is not None:
        text += f'<b>Время выполнения:</b> {order.time}\n'

    if order.underground is not None:
        text += f'<b>Ближайшая станция метро ({round(order.underground_distance, 2)} км до нее):</b> {order.underground}\n'

    photos = []
    for i in range(1, 7):
        photo = getattr(order, f'photo_{i}', 'null')
        if photo is not None:
            photos.append(InputMediaPhoto(media=photo))

    return text, photos


def get_user_self_template(user_profile):
    text = f'''<b>Имя</b>: {user_profile.name}\n'''
    text += f'<b>Возраст</b>: {user_profile.age}'
    if user_profile.description is not None:
        text += f'<b>\nОписание</b>: {user_profile.description}'
    if user_profile.phone_number is not None:
        text += f'\n<b>Номер телефона</b>: {user_profile.phone_number}'
    return text


def get_user_template(user_profile, role, order_name=None):
    text = ''

    if role == 'executor':
        text += f'Мы нашли для вас исполнителя на заказ "{order_name}"!\n\n'
        text += f'<b>Исполнитель</b>: <a href="tg://user?id={user_profile.user_id}">{user_profile.name}</a>'
    elif role == 'creator':
        text += f'<b>Заказчик</b>: <a href="tg://user?id={user_profile.user_id}">{user_profile.name}</a>'

    if user_profile.description is not None:
        text += f'\n{user_profile.description}'

    text += f'\n<b>Возраст</b>: {user_profile.age}'

    if user_profile.phone_number is not None:
        text += f'\n<b>Номер телефона</b>: {user_profile.phone_number}'

    if user_profile.username is not None:
        text += f'\n@{user_profile.username}'

    text += f'\n\nВам следует связаться с ним и договорится обо всех подробностях и условиях заказа.\n\n'

    if role == 'executor':
        text += f'Отказаться от работника или завершить заказ вы можете в списке своих заказов (/my_orders)'

    elif role == 'creator':
        text += f'Отказаться от заказа или завершить его вы можете в списке своих заказов (/my_orders)'

    return text




