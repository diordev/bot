from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

login = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Login", callback_data="login")
        ]
    ]
)
