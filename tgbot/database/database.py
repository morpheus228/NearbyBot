import asyncpg
import logging
from tgbot.database.schemas import Order, User, UserProfile, Request

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self, config):
        self.pool = await asyncpg.create_pool(
            user=config.user,
            password=config.password,
            database=config.database,
            host=config.host)

    async def execute(self, sql, ignore_error=None, parse_none=True):
        if parse_none:
            sql = sql.replace("'None'", "None").replace('None', 'null')

        if ignore_error is None:
            await self.pool.execute(sql)

        elif ignore_error == 'print_all':
            try:
                await self.pool.execute(sql)
            except BaseException as error:
                print(f'ERROR: {error}')

        else:
            try:
                await self.pool.execute(sql)
            except ignore_error:
                pass

    async def fetchrow(self, sql, ignore_error=None):
        if ignore_error is None:
            return await self.pool.fetchrow(sql)

        elif ignore_error == 'print_all':
            try:
                return await self.pool.fetchrow(sql)
            except BaseException as error:
                print(f'ERROR: {error}')

        else:
            try:
                return await self.pool.fetchrow(sql)
            except ignore_error:
                pass

    async def fetch(self, sql, ignore_error=None):
        if ignore_error is None:
            return await self.pool.fetch(sql)

        elif ignore_error == 'print_all':
            try:
                return await self.pool.fetch(sql)
            except BaseException as error:
                print(f'ERROR: {error}')

        else:
            try:
                return await self.pool.fetch(sql)
            except ignore_error:
                pass

    async def add_message_event(self, message):
        sql = f'''INSERT INTO message_events (
              id, text, time, user_id, chat_id)
              VALUES (
              {message.message_id}, '{message.text}', NOW(), {message.from_user.id}, {message.chat.id});'''

        await self.execute(sql)

    async def add_callback_event(self, call):
        sql = f'''INSERT INTO callback_events (
              id, message_id, data, text, 
              time, user_id, chat_id)
              VALUES (
              {call.id}, '{call.message.message_id}', '{call.data}', '{call.message.text}', 
              NOW(), {call.from_user.id}, {call.message.chat.id});'''

        await self.execute(sql)

    async def add_request(self, order, message_id, requester):
        sql = f'''INSERT INTO requests (
              message_id, order_id, creator_id, executor_id, requester, created_at, action)
              VALUES (
              {message_id}, {order.id}, {order.creator_id}, {order.executor_id}, '{requester}', NOW(), 'completing');'''

        await self.execute(sql)

    async def get_order_by_id(self, order_id):
        sql = f'''SELECT
        name, description, address, time, underground, 
        underground_distance, price, status, latitude, longitude,
        photo_1, photo_2, photo_3, photo_4, photo_5, photo_6,
        creator_id, executor_id, id
        FROM orders WHERE id = {order_id};'''

        row = await self.fetchrow(sql)
        return Order().load_from_db(row)

    async def get_user_by_id(self, user_id):
        sql = f'''SELECT
        id, is_bot, first_name, username, last_name, language_code
        FROM users WHERE id = {user_id}'''

        row = await self.fetchrow(sql)
        return User().load_from_db(row)

    async def get_user_profile_by_id(self, user_id):
        sql = f'''SELECT
        id, name, age, description, phone_number, username
        FROM users WHERE id = {user_id}'''

        row = await self.fetchrow(sql)
        return UserProfile().load_from_db(row)

    async def get_orders_with_location(self, executor_id):
        sql = f'''SELECT id, latitude, longitude FROM orders WHERE status = 1 AND  creator_id != {executor_id};'''
        rows = await self.fetch(sql)
        return [(row[0], (row[1], row[2])) for row in rows]

    async def get_orders_as_creator(self, user_id):
        sql = f'''SELECT id FROM orders WHERE (creator_id={user_id}) and (status != 3);'''
        rows = await self.fetch(sql)
        orders = [await self.get_order_by_id(row[0]) for row in rows]
        return orders

    async def get_orders_as_executor(self, user_id):
        sql = f'''SELECT id FROM orders WHERE (executor_id={user_id}) and (status != 3);'''
        rows = await self.fetch(sql)
        orders = [await self.get_order_by_id(row[0]) for row in rows]
        return orders

    async def get_request_by_message_id(self, message_id):
        sql = f'''SELECT (message_id, order_id, requester, action, agreement) FROM requests WHERE message_id={message_id};'''
        row = await self.fetchrow(sql)
        return Request().load_from_db(row[0])

    async def get_active_request(self, order_id, user_id, requester):
        sql = f'''SELECT message_id FROM requests 
        WHERE order_id={order_id} AND requester='{requester}' AND {requester+'_id'} = {user_id} AND agreement is null;'''
        rows = [row[0] for row in await self.fetch(sql)]
        return rows

    async def delete_order(self, order_id):
        sql = f'DELETE FROM orders WHERE id = {order_id};'
        await self.execute(sql)

    async def alter_order(self, order_id, **kwargs):
        sql = 'UPDATE orders SET '
        for key in kwargs:
            value = kwargs[key]
            if type(value) is str:
                sql += f"{key} = '{kwargs[key]}', "
            else:
                sql += f"{key} = {kwargs[key]}, "

        sql += 'updated_at = NOW() '
        sql += f'WHERE id={order_id};'
        await self.execute(sql)

    async def alter_user(self, user_id, **kwargs):
        sql = 'UPDATE users SET '
        for key in kwargs:
            value = kwargs[key]
            if type(value) is str:
                sql += f"{key} = '{kwargs[key]}', "
            else:
                sql += f"{key} = {kwargs[key]}, "

        sql += 'updated_at = NOW() '
        sql += f'WHERE id={user_id};'
        await self.execute(sql)

    async def finish_request(self, message_id, agreement):
        sql = f'''UPDATE requests SET
              agreement = {agreement},
              answered_at = NOW()
              WHERE message_id = {message_id};'''

        await self.execute(sql)

    async def is_user_registered(self, user_id):
        sql = f'''SELECT registered FROM users WHERE id = {user_id};'''
        registered = (await self.pool.fetchrow(sql))[0]
        return registered

    async def check_order_availability(self, order_id):
        sql = f'SELECT status FROM orders WHERE id={order_id}'
        row = await self.fetchrow(sql)
        return (row is not None) and (row[0] == 1)




