from aiogram.dispatcher.filters.state import StatesGroup, State


class AddWorker(StatesGroup):
    user_type = State()
    first_name = State()
    last_name = State()
    username = State()
    password = State()
    photo = State()


class EditWorker(StatesGroup):
    first_name = State()
    last_name = State()
    username = State()
    password = State()
    photo = State()
