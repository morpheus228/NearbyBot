from tgbot.config import MAX_ORDERS_COUNT_AS_CREATOR, MAX_ORDERS_COUNT_AS_EXECUTOR


async def check_orders_count_for_creator(user_id, db):
    orders = await db.get_orders_as_creator(user_id)
    return len(orders) < MAX_ORDERS_COUNT_AS_CREATOR


async def check_orders_count_for_executor(user_id, db):
    orders = await db.get_orders_as_executor(user_id)
    return len(orders) < MAX_ORDERS_COUNT_AS_EXECUTOR
