from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.user_type import admin_filter
from keyboards.inline.workersList import get_workers_list, add_worker_btn
from loader import dp, db


@dp.callback_query_handler(text="menuworker_list", state="*")
@dp.message_handler(admin_filter, text="Xodimlar")
async def worker_list(message: types.Message, state: FSMContext):
    await state.finish()
    company_id = (await db.select_user(telegram_id=message.from_user.id, auth_status=True))['company_id']
    workers = await db.select_users_without_admin(company_id=company_id)
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
        message = message.message
    if workers:
        company_name = (await db.select_company(id=company_id))['name']
        workers_list = f'<b><em>"{company_name}"</em>  kompaniyasining xodimlari:</b>\n\n'
        for i, worker in enumerate(workers):
            workers_list += f"{i + 1}. {worker['first_name']} {worker['last_name']}  <em>({worker['user_type']})</em>\n"
        workers_list += "\n\n\n<em>Batafsil ma'lumot uchun xodimning ID sini bosing</em>"
        buttons = await get_workers_list(company_id=company_id)
        await message.answer(workers_list, parse_mode="HTML", reply_markup=buttons)
    else:
        btn = types.InlineKeyboardMarkup(inline_keyboard=[[add_worker_btn]])
        await message.answer("Xodimlar mavjud emas!", reply_markup=btn)
