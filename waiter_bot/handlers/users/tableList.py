from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from filters.user_type import waiter_filter, cashier_filter
from keyboards.inline.tableList import get_table_list, add_table_btn, get_ordered_table_list
from loader import dp, db


@dp.callback_query_handler(text="menutable_list", state="*")
@dp.message_handler(waiter_filter, text="Stollar", state="*")
async def table_list(message: types.Message, state: FSMContext):
    await state.finish()
    company_id = (await db.select_user(telegram_id=message.from_user.id, auth_status=True))['company_id']
    tables = await db.select_tables(company_id=company_id)
    add_btn = InlineKeyboardMarkup(inline_keyboard=[[add_table_btn]])
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
        message = message.message
    if tables:
        tables_list = f"<b>Stollar:</b>\n\n"
        for i, table in enumerate(tables):
            tables_list += f"<b>{i + 1}.</b> {table['name']}\n"
        tables_list += "\n<b>Stolni tanlang:</b>"
        btn = await get_table_list(company_id=company_id)
        await message.answer(tables_list, parse_mode="HTML", reply_markup=btn)
    else:
        await message.answer("Stollar mavjud emas!", reply_markup=add_btn)


@dp.callback_query_handler(text="menucashiertable_list", state="*")
@dp.message_handler(cashier_filter, text="Stollar", state="*")
async def table_list(message: types.Message, state: FSMContext):
    await state.finish()
    company_id = (await db.select_user(telegram_id=message.from_user.id, auth_status=True))['company_id']
    tables = await db.select_tables(company_id=company_id, is_active=True)
    print(tables, company_id)
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
        message = message.message
    if tables:
        tables_list = f"<b>Stollar:</b>\n\n"
        for i, table in enumerate(tables):
            tables_list += f"<b>{i + 1}.</b> {table['name']}\n"
        tables_list += "\n<b>Stolni tanlang:</b>"
        btn = await get_ordered_table_list(company_id=company_id)
        await message.answer(tables_list, parse_mode="HTML", reply_markup=btn)
    else:
        await message.answer("Buyurtma berilgan stollar mavjud emas!")
