from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

add_order_btn = InlineKeyboardButton(text="Buyurtma qo'shish", callback_data="add_order")


async def get_order_list(company_id: int, waiter_id: int) -> InlineKeyboardMarkup:
    tables = await db.select_not_empty_tables(company_id=company_id)
    btn = InlineKeyboardMarkup(row_width=2)
    for table in tables:
        order = await db.select_order(table_id=table['id'], waiter_id=waiter_id, status="in_process")
        if order:
            btn.insert(InlineKeyboardButton(text=table['name'], callback_data=f"order:{table['id']}"))
    btn.row(add_order_btn)
    return btn

