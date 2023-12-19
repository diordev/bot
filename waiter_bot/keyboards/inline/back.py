from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_btn(menu: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text="Orqaga", callback_data=menu)


def back_markup(menu: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(back_btn(menu))
    return markup
