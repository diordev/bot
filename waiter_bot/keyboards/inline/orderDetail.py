from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.back import back_btn


async def get_order_detail(table_id: int) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    buttons.add(
        InlineKeyboardButton(text="O'chirish", callback_data=f"deleteOrder:{table_id}"),
        InlineKeyboardButton(text="Mahsulot qo'shish", callback_data=f"updateOrder:{table_id}")
    )
    buttons.add(back_btn(menu="menuorder_list"))
    return buttons
