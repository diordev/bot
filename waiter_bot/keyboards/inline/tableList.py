from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

add_table_btn = InlineKeyboardButton(text="Stol qo'shish", callback_data="addtable")


async def get_table_list(company_id: int) -> InlineKeyboardMarkup:
    tables = await db.select_tables(company_id=company_id)
    tables_list = InlineKeyboardMarkup(row_width=2)
    for table in tables:
        tables_list.insert(InlineKeyboardButton(text=table['name'], callback_data=f"detailtable:{table['id']}"))
    tables_list.row(add_table_btn)
    return tables_list


async def get_ordered_table_list(company_id: int) -> InlineKeyboardMarkup:
    tables = await db.select_tables(company_id=company_id, is_active=True)
    tables_list = InlineKeyboardMarkup(row_width=2)
    for table in tables:
        tables_list.insert(InlineKeyboardButton(text=table['name'], callback_data=f"table_order:{table['id']}"))
    return tables_list

table_list_btn = InlineKeyboardMarkup()
table_list_btn.add(InlineKeyboardButton(text="Stollar", callback_data="menutable_list"))