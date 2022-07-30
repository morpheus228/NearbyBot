from aiogram.dispatcher.filters.state import StatesGroup, State


# Список состоний для регистрации пользователя
class UserRegistration(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    description = State()
    notifications = State()
    location = State()


# Список состоний для создания нового заказа
class OrderCreating(StatesGroup):
    name = State()
    description = State()

    first_photo = State()
    second_photo = State()
    third_photo = State()
    fourth_photo = State()
    fifth_photo = State()
    sixth_photo = State()

    price = State()
    address = State()
    underground_station = State()
    time = State()

    confirmation = State()


class FindOrder(StatesGroup):
    location = State()
    order = State()


class MyOrders(StatesGroup):
    role = State()
    orders_as_creator = State()
    orders_as_executor = State()
    order_as_creator = State()
    order_as_executor = State()


class MyProfile(StatesGroup):
    action = State()
    name = State()
    age = State()
    phone_number = State()
    description = State()


class Settings(StatesGroup):
    action = State()
    location = State()
