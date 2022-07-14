from dataclasses import dataclass


@dataclass
class UserRegistration:
    name = 'Как вас зовут?'
    age = 'Сколько вам лет?'
    phone_number = 'Укажите свой номер телефона, чтобы заказчик или работник точно смогли с вами связаться'
    description = 'Напишите пару слов о себе (сильные стороны, навыки, умения), чтобы заказчик или работник понимали с кем сотрудничают'


@dataclass
class MyProfile:
    name_successfully = 'Вы успешно сменили имя профиля!'
    age_successfully = 'Вы успешно сменили возраст профиля!'
    phone_number_successfully = 'Вы успешно сменили номер телефона профиля!'
    description_successfully = 'Вы успешно сменили краткое описание профиля!'
    profile_successfully = 'Вы успешно изменили свой профиль!'


@dataclass
class General:
    menu = "Главное меню:"


user_registration = UserRegistration()
my_profile = MyProfile()
general = General()
