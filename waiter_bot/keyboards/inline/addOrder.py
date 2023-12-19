from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def get_empty_table_list(company_id: int) -> InlineKeyboardMarkup:
    tables = await db.select_empty_tables(company_id=company_id)
    btn = InlineKeyboardMarkup(row_width=2)
    for table in tables:
        btn.insert(InlineKeyboardButton(text=table['name'], callback_data=f"addOrder:{table['id']}"))
    return btn


async def get_product_list(company_id: int) -> InlineKeyboardMarkup:
    products = await db.select_products(company_id=company_id)
    btn = InlineKeyboardMarkup(row_width=2)
    for product in products:
        btn.insert(InlineKeyboardButton(text=product['name'], callback_data=f"addOrderProduct:{product['id']}"))
    return btn


async def get_product_unit(product_id: int) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(text="kg", callback_data=f"{product_id}:unit:kg"))
    buttons.add(InlineKeyboardButton(text="gram", callback_data=f"{product_id}:unit:gram"))
    return buttons


async def get_product_quantity(product_id: int, quantity: Union[int, str]) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    if not quantity:
        quantity = 1
    buttons.row(
        InlineKeyboardButton(text="-", callback_data=f"{product_id}:addOrderQuantity:-"),
        InlineKeyboardButton(text=f"{quantity}", callback_data=f"{product_id}:addOrderQuantity:{quantity}"),
        InlineKeyboardButton(text="+", callback_data=f"{product_id}:addOrderQuantity:+")
    )
    buttons.row(InlineKeyboardButton(text="Submit", callback_data=f"{product_id}:addOrderQuantity:Submit"))
    return buttons


add_order_keyboard = InlineKeyboardMarkup(row_width=1)
add_order_keyboard.row(InlineKeyboardButton(text="Yana mahsulot qo'shish", callback_data="add_new_product"))
add_order_keyboard.row(InlineKeyboardButton(text="Buyurtma qilish", callback_data="finish_order"))

service_charge_keyboard = InlineKeyboardMarkup(row_width=2)
service_charge_keyboard.add(InlineKeyboardButton(text="0%", callback_data=f"service_charge:0"))
service_charge_keyboard.add(InlineKeyboardButton(text="5%", callback_data=f"service_charge:5"))
service_charge_keyboard.add(InlineKeyboardButton(text="10%", callback_data=f"service_charge:10"))
service_charge_keyboard.add(InlineKeyboardButton(text="15%", callback_data=f"service_charge:15"))
service_charge_keyboard.add(InlineKeyboardButton(text="20%", callback_data=f"service_charge:20"))


async def get_confirm_keyboard(table_id: int) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup(row_width=2)
    buttons.add(InlineKeyboardButton(text="Ha", callback_data=f"order_confirm:{table_id}"))
    buttons.add(InlineKeyboardButton(text="Yo'q", callback_data=f"order_cancel:{table_id}"))
    return buttons


async def get_cook_keyboard(table_id: int) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(text="Tayyor!", callback_data=f"cookorder:{table_id}"))
    return buttons