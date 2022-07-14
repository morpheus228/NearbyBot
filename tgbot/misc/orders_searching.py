from tgbot.misc.geo import calc_distance


async def find_nearest_orders(db, user_location):
    orders = await db.get_orders_with_location()
    orders = [(order[0], calc_distance(user_location, order[1])) for order in orders]
    orders = sorted(orders, key=lambda x: x[1])
    return orders
