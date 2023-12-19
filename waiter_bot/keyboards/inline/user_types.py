from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

usertypes_callback = CallbackData("user_types", "user_type")

user_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cashier", callback_data=usertypes_callback.new(user_type="cashier")),
            InlineKeyboardButton(text="Waiter", callback_data=usertypes_callback.new(user_type="waiter"))
        ],
    ]
)
