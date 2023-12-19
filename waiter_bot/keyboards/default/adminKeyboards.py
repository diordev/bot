from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

worker = ReplyKeyboardMarkup(resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton("Mahsulotlar"),
                                     KeyboardButton("Xodimlar"),
                                 ],
                                 [
                                     KeyboardButton("Buyurtmalar"),
                                     KeyboardButton("Statistika")
                                 ]
                             ]
                             )
