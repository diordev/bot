from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    table = State()
    product = State()
    unit = State()
    quantity = State()
