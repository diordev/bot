from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.back import back_btn

table_detail_btn = CallbackData("table", "action", "table_id")
edit_table_btn = CallbackData("edit_table", "field")


async def get_table_detail_btn(table_id: int) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    buttons.insert(InlineKeyboardButton(text="Stolni o'chirish",
                                        callback_data=table_detail_btn.new(action="del", table_id=table_id)))
    buttons.insert(InlineKeyboardButton(text="Stolni yangilash",
                                        callback_data=table_detail_btn.new(action="update", table_id=table_id)))
    buttons.row(back_btn(menu="menutable_list"))
    return buttons


async def get_edit_table_btn(table_id: int) -> InlineKeyboardMarkup:
    skip_btn = InlineKeyboardMarkup()
    skip_btn.insert(InlineKeyboardButton(text="Skip", callback_data="edittablename"))
    skip_btn.insert(back_btn(menu=f"detailtable:{table_id}"))
    return skip_btn
