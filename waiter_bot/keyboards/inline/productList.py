from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

add_product_btn = InlineKeyboardButton(text="Mahsulot qo'shish", callback_data=f"addproduct")


async def get_products_list(company_id: int, category_id: int) -> InlineKeyboardMarkup:
    products = await db.select_products(company_id=company_id, category_id=category_id)
    prd = [InlineKeyboardButton(text=f"{product[3]}", callback_data=f"productlist:{product[0]}") for i, product in
           enumerate(products)]
    products_list = InlineKeyboardMarkup()
    products_list.row(InlineKeyboardButton(
                text="Mahsulot qo'shish",
                callback_data=f"addproduct:{category_id}"))
    products_list.add(*prd)
    return products_list
