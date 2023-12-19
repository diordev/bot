from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

worker_detail_btn = CallbackData("worker", "action", "worker_id")
edit_worker_btn = CallbackData("edit_worker", "field")