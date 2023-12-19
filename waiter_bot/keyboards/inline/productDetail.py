from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.back import back_btn

product_detail_btn = CallbackData("product", "action", "product_id")
edit_product_btn = CallbackData("edit_product", "field")

choice_unit = InlineKeyboardMarkup()
choice_unit.insert(InlineKeyboardButton(text="Kilo", callback_data="unit:kg"))
choice_unit.insert(InlineKeyboardButton(text="Dona", callback_data="unit:piece"))


async def get_product_detail_keyboard(product_id: int, category_id: Union[int, str]) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    buttons.insert(InlineKeyboardButton(text="Mahsulotni o'chirish",
                                        callback_data=product_detail_btn.new(action="del", product_id=product_id)))
    buttons.insert(InlineKeyboardButton(text="Mahsulotni yangilash",
                                        callback_data=product_detail_btn.new(action="update", product_id=product_id)))
    buttons.row(back_btn(menu=f"catlist:{category_id}"))
    return buttons


async def get_edit_product_keyboard(product_id: int) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    buttons.insert(InlineKeyboardButton(text="Skip", callback_data=edit_product_btn.new(field="name")))
    buttons.insert(InlineKeyboardButton(text="Orqaga", callback_data=f"productlist:{product_id}"))
    return buttons


async def get_edit_skip_btn(field: str) -> InlineKeyboardMarkup:
    button = InlineKeyboardMarkup()
    button.insert(InlineKeyboardButton(text="Skip", callback_data=edit_product_btn.new(field=field)))
    return button