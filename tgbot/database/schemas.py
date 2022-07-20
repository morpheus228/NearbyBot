from dataclasses import dataclass
from abc import ABC, abstractmethod

from asyncpg import UniqueViolationError


class DatabaseObject(ABC):
    def __init__(self):
        self.defined_variables = []

    @abstractmethod
    def save(self, db):
        pass

    def load_from_data(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])

        return self


class User(DatabaseObject, ABC):
    age_limit = 120
    name_length_limit = 50
    description_length_limit = 5000

    def __init__(self):
        super().__init__()
        self.id = None
        self.is_bot = None
        self.first_name = None
        self.username = None
        self.last_name = None
        self.language_code = None

    def load_from_tg_user(self, user):
        self.id = user.id
        self.is_bot = user.is_bot
        self.first_name = user.first_name
        self.username = user.username
        self.last_name = user.last_name
        self.language_code = user.language_code
        return self

    async def save(self, db):
        sql = f'''INSERT INTO users (id, is_bot, first_name, username, last_name, language_code, registered, created_at)
        VALUES ({self.id}, {self.is_bot}, '{self.first_name}', '{self.username}', '{self.last_name}', 
        '{self.language_code}', false, NOW());'''

        await db.execute(sql, ignore_error=UniqueViolationError)
        return self

    def load_from_db(self, row):
        self.id = row[0]
        self.is_bot = row[1]
        self.first_name = row[2]
        self.username = row[3]
        self.last_name = row[4]
        self.language_code = row[5]
        return self


class UserProfile(DatabaseObject, ABC):
    age_limit = 120
    name_length_limit = 50
    description_length_limit = 5000

    def __init__(self):
        super().__init__()
        self.user_id = None
        self.name = None
        self.username = None
        self.age = None
        self.description = None
        self.phone_number = None
        self.notifications = None
        self.latitude = None
        self.longitude = None
        self.notifications = None

    async def save(self, db):
        sql = f'''UPDATE users SET
        name = '{self.name}', 
        description = '{self.description}',
        age = {self.age},
        phone_number = '{self.phone_number}',
        notifications = {self.notifications},
        latitude = {self.latitude},
        longitude = {self.longitude},
        registered = true
        WHERE id = {self.user_id};'''

        await db.execute(sql)
        return self

    def load_from_db(self, row):
        self.user_id = row[0]
        self.name = row[1]
        self.age = row[2]
        self.description = row[3]
        self.phone_number = row[4]
        self.username = row[5]
        self.latitude = row[6]
        self.longitude = row[7]
        self.notifications = row[8]

        return self


class Order(DatabaseObject):
    name_length_limit = 150
    description_length_limit = 1500
    photo_length_limit = 100
    address_length_limit = 100
    price_limit = 10000
    underground_length_limit = 100
    time_length_limit = 100

    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.description = None
        self.address = None
        self.time = None
        self.underground = None
        self.underground_distance = None
        self.price = None
        self.status = None
        self.latitude = None
        self.longitude = None
        self.photo_1 = None
        self.photo_2 = None
        self.photo_3 = None
        self.photo_4 = None
        self.photo_5 = None
        self.photo_6 = None
        self.creator_id = None
        self.executor_id = None

    async def save(self, db):
        sql = f'''
        INSERT INTO orders (
        name, description, address, time, underground, 
        underground_distance, price, status, latitude, longitude,
        photo_1, photo_2, photo_3, photo_4, photo_5, photo_6,
        creator_id, executor_id, created_at)
        VALUES (
        '{self.name}', '{self.description}', '{self.address}', '{self.time}', '{self.underground}', 
        {self.underground_distance},  {self.price},  {self.status},  {self.latitude},  {self.longitude},
        '{self.photo_1}', '{self.photo_2}', '{self.photo_3}', '{self.photo_4}', '{self.photo_5}', '{self.photo_6}',
        {self.creator_id}, {self.executor_id}, NOW())
        RETURNING id;'''

        row = await db.fetchrow(sql)
        self.id = row[0]
        return self

    def load_from_db(self, row):
        self.name = row[0]
        self.description = row[1]
        self.address = row[2]
        self.time = row[3]
        self.underground = row[4]
        self.underground_distance = row[5]
        self.price = row[6]
        self.status = row[7]
        self.latitude = row[8]
        self.longitude = row[9]
        self.photo_1 = row[10]
        self.photo_2 = row[11]
        self.photo_3 = row[12]
        self.photo_4 = row[13]
        self.photo_5 = row[14]
        self.photo_6 = row[15]
        self.creator_id = row[16]
        self.executor_id = row[17]
        self.id = row[18]

        return self


class Request:
    def __init__(self):
        self.message_id = None
        self.order_id = None
        self.requester = None
        self.action = None
        self.agreement = None

    def load_from_db(self, row):
        self.message_id = row[0]
        self.order_id = row[1]
        self.requester = row[2]
        self.action = row[3]
        self.agreement = row[4]
        return self

    def save(self):
        pass


class Notification:
    def __init__(self):
        self.message_id = None
        self.order_id = None
        self.accept = None

    def load_from_db(self, row):
        self.message_id = row[0]
        self.order_id = row[1]
        self.accept = row[2]
        return self

    def save(self):
        pass


# class User(DatabaseObject):
#     id: int
#     is_bot: bool
#     first_name: str
#     username: str
#     last_name: str
#     language_code: str
#
#     age: int
#     age_limit = 120
#
#     phone_number: str
#
#     name: str
#     name_length_limit = 50
#
#     description: str
#     description_length_limit = 5000

# @dataclass
# class Order:
#     name: str
#     name_length_limit = 150
#
#     description: str
#     description_length_limit = 1500
#
#     photo_1: str
#     photo_2: str
#     photo_3: str
#     photo_4: str
#     photo_5: str
#     photo_6: str
#     photo_length_limit = 100
#
#     address: str
#     address_length_limit = 100
#
#     price: int
#     price_limit = 10000
#
#     time: str
#     time_length_limit = 100
#
#     underground: str
#     underground_length_limit = 100
#
#     status: int
#     latitude: float
#     longitude: float




