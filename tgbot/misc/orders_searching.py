from tgbot.misc.geo import calc_distance


async def find_nearest_orders(db, user_location, executor_id):
    orders = await db.get_orders_with_location(executor_id)
    orders = [(order[0], calc_distance(user_location, order[1])) for order in orders]
    orders = filter(lambda x: x[1] < 10, orders)
    orders = sorted(orders, key=lambda x: x[1])
    return orders
