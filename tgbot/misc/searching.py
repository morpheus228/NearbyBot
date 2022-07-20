from tgbot.config import ORDER_AVAILABILITY_RADIUS
from tgbot.misc.geo import calc_distance


async def find_nearest_orders(db, user_location, executor_id):
    orders = await db.get_orders_with_location(executor_id)
    orders = [(order[0], calc_distance(user_location, order[1])) for order in orders]
    orders = filter(lambda x: x[1] < ORDER_AVAILABILITY_RADIUS, orders)
    orders = sorted(orders, key=lambda x: x[1])
    return orders


async def find_users_for_mailing(order, db):
    users = await db.get_sending_users_with_location(order.creator_id)
    users = [(user[0], calc_distance((order.latitude, order.longitude), user[1])) for user in users]
    users = filter(lambda x: x[1] < ORDER_AVAILABILITY_RADIUS, users)
    users = sorted(users, key=lambda x: x[1])
    return users