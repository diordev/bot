from aiogram.dispatcher.filters.state import StatesGroup, State


class Login(StatesGroup):
    username = State()
    password = State()
