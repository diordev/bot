from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cashier_actions = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                      keyboard=[
                                          [
                                              KeyboardButton("Stollar")
                                          ]
                                      ]
                                      )
