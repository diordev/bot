from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTable(StatesGroup):
    name = State()


class EditTable(StatesGroup):
    name = State()
