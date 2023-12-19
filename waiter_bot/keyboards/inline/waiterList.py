from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def get_waiter_list(company_id: int, date_range: str) -> InlineKeyboardMarkup:
    waiter_list = await db.select_users(company_id=company_id, user_type='waiter')
    result = InlineKeyboardMarkup(row_width=1)
    if waiter_list:
        for waiter in waiter_list:
            result.add(InlineKeyboardButton(text=f"{waiter['first_name']} {waiter['last_name']}",
                                            callback_data=f"{date_range}_waiter_{waiter['id']}"))
    return result

