from aiogram.types import InlineKeyboardMarkup

from loader import db
from aiogram import types


async def get_categories(company_id: int) -> InlineKeyboardMarkup:
    categories = await db.select_categories(company_id=company_id)
    buttons = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        buttons.insert(types.InlineKeyboardButton(text=category['name'], callback_data=f"category:{category['id']}"))
    return buttons


async def get_categories_list(company_id: int) -> InlineKeyboardMarkup:
    categories = await db.select_categories(company_id=company_id)
    buttons = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        buttons.insert(types.InlineKeyboardButton(text=category['name'], callback_data=f"catlist:{category['id']}"))
    return buttons
