from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.back import back_btn
from keyboards.inline.user_types import usertypes_callback
from loader import db

add_worker_btn = InlineKeyboardButton(
    text="Xodim qo'shish",
    callback_data=f"addworker"
)

add_worker_user_type = InlineKeyboardMarkup(row_width=2)
add_worker_user_type.add(InlineKeyboardButton("Oshpaz", callback_data=usertypes_callback.new(user_type="cook")))
add_worker_user_type.add(InlineKeyboardButton("Kassir", callback_data=usertypes_callback.new(user_type="cashier")),
                         InlineKeyboardButton("Ofitsiant", callback_data=usertypes_callback.new(user_type="waiter")))
add_worker_user_type.add(back_btn(menu="menuworker_list"))


async def get_workers_list(company_id: int) -> InlineKeyboardMarkup:
    workers = await db.select_users(company_id=company_id, user_type="waiter")
    workers += await db.select_users(company_id=company_id, user_type="cashier")
    workers += await db.select_users(company_id=company_id, user_type="cook")
    workers_list = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Xodim qo'shish",
                callback_data=f"addworker"
            )],
            [InlineKeyboardButton(text=f"{i + 1}", callback_data=f"workerlist:{worker[0]}") for i, worker in
             enumerate(workers)]

        ], row_width=2
    )
    return workers_list
