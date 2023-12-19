from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.user_type import waiter_filter
from keyboards.inline.back import back_markup
from keyboards.inline.tableList import table_list_btn
from loader import dp, db
from states.addTable import AddTable


@dp.callback_query_handler(waiter_filter, text="addtable")
@dp.callback_query_handler(state=AddTable.name)
async def add_table(call: types.CallbackQuery):
    await call.message.delete()
    back = back_markup(menu='menutable_list')
    await call.message.answer("Yangi stol nomini kiriting:", reply_markup=back)
    await AddTable.name.set()


@dp.message_handler(waiter_filter, state=AddTable.name)
async def add_table_name(message: types.Message, state: FSMContext):
    name = message.text
    table = await db.select_table(name=name)
    if table:
        await message.answer("Bunday stol mavjud!")
        return
    company_id = (await db.select_user(telegram_id=message.from_user.id, auth_status=True))['company_id']
    await db.create_new_table(company_id=company_id, name=name)
    await state.finish()
    msg = "Yangi stol qo'shildi"
    msg += f'\n\n<b>Stol nomi:</b> {name}'
    msg += "\nStollar ro'yxatini ko'rish uchun <em>Stollar</em> tugmasini bosing"
    await message.answer(msg, parse_mode="HTML", reply_markup=table_list_btn)

