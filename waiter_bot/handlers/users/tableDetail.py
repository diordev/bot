from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.user_type import waiter_filter
from keyboards.inline.tableDetail import table_detail_btn, get_table_detail_btn, get_edit_table_btn
from loader import db, dp
from states.addTable import EditTable


@dp.callback_query_handler(waiter_filter, table_detail_btn.filter(action="del"))
async def delete_table(call: types.CallbackQuery, callback_data: dict):
    table_id = int(callback_data['table_id'])
    await db.delete_table(id=table_id)
    await call.message.delete()
    await call.message.answer("Stol o'chirildi")
    await call.answer()


@dp.callback_query_handler(waiter_filter, table_detail_btn.filter(action="update"), state="*")
async def update_table(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    table_id = int(callback_data['table_id'])
    await call.message.delete()
    await state.update_data(table_id=table_id)
    buttons = await get_edit_table_btn(table_id=table_id)
    await call.message.answer("Yangi stol nomini kiriting:", reply_markup=buttons)
    await EditTable.name.set()
    await call.answer()


@dp.message_handler(waiter_filter, state=EditTable.name)
async def edit_table_name(message: types.Message, state: FSMContext):
    name = message.text
    table_id = (await state.get_data())['table_id']
    await db.update_table(table_id=table_id, name=name)
    await state.finish()
    await message.answer("Stol nomi yangilandi")


@dp.callback_query_handler(waiter_filter, text="edittablename", state=EditTable.name)
async def skip_edit_table_name(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Yangilanish bekor qilindi")
    await call.answer()


@dp.callback_query_handler(waiter_filter, lambda call: call.data.startswith("detailtable:"))
@dp.callback_query_handler(state=EditTable.name)
async def table_detail(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    await state.finish()
    table_id = int(call.data.split(":")[-1])
    table = await db.select_table(id=table_id)
    buttons = await get_table_detail_btn(table_id=table_id)
    await call.message.delete()
    await call.message.answer(f"<b>Stol nomi:</b> {table['name']}\n", parse_mode="HTML", reply_markup=buttons)
