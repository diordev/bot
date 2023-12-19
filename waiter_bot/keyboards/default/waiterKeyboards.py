from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

waiter_actions = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                     keyboard=[
                                         [
                                             KeyboardButton("Mahsulotlar"),
                                             KeyboardButton("Buyurtmalar"),
                                         ],
                                         [
                                             KeyboardButton("Stollar"),
                                         ]
                                     ]
                                     )
