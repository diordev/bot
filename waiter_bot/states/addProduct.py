from aiogram.dispatcher.filters.state import StatesGroup, State


class Product(StatesGroup):
    name = State()
    unit = State()
    price = State()
    description = State()
    photo = State()


class EditProduct(StatesGroup):
    name = State()
    price = State()
    description = State()
    photo = State()
