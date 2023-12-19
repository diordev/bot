from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.user_type import admin_filter
from keyboards.inline.WorkerDetail import worker_detail_btn, edit_worker_btn
from keyboards.inline.back import back_btn
from loader import dp, db, bot
from states.addWorker import EditWorker
from utils.send_photo import user_photo


@dp.callback_query_handler(admin_filter, lambda call: call.data.startswith("workerlist:"))
@dp.callback_query_handler(lambda call: call.data.startswith("workerlist:"), state=EditWorker.first_name)
async def worker_detail(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    worker_id = call.data.split(":")[1]
    worker = await db.select_user(id=int(worker_id))
    company = await db.select_company(id=worker['company_id'])
    worker_detail_msg = f"<b>Xodim haqida ma'lumot:</b>\n\n" \
                        f"<b>Ismi:</b> {worker['first_name']}\n" \
                        f"<b>Familiyasi:</b> {worker['last_name']}\n" \
                        f"<b>Username:</b> {worker['username']}\n" \
                        f"<b>Kompaniya nomi:</b> {company['name']}\n" \
                        f"<b>Xodim turi:</b> {worker['user_type']}\n"
    del_worker_btn = types.InlineKeyboardMarkup()
    del_worker_btn.insert(types.InlineKeyboardButton(text="Xodimni o'chirish",
                                                     callback_data=worker_detail_btn.new(action="del",
                                                                                         worker_id=worker_id)))
    del_worker_btn.insert(types.InlineKeyboardButton(text="Xodimni yangilash",
                                                     callback_data=worker_detail_btn.new(action="edit",
                                                                                         worker_id=worker_id)))
    del_worker_btn.row(back_btn(menu="menuworker_list"))
    if worker['photo']:
        photo = await user_photo(worker['photo'])
        await call.message.delete()
        await call.message.answer_photo(photo, worker_detail_msg, parse_mode="HTML", reply_markup=del_worker_btn)
    else:
        await call.message.delete()
        await call.message.answer(worker_detail_msg, parse_mode="HTML", reply_markup=del_worker_btn)
    await call.answer()


@dp.callback_query_handler(admin_filter, worker_detail_btn.filter(action="del"))
async def del_worker(call: types.CallbackQuery, callback_data: dict):
    worker_id = callback_data['worker_id']
    await db.delete_user(id=int(worker_id))
    await call.message.delete()
    await call.message.answer("Xodim o'chirildi")
    await call.answer()


@dp.callback_query_handler(admin_filter, worker_detail_btn.filter(action="edit"))
@dp.callback_query_handler(state=EditWorker.first_name, text="Orqaga")
async def edit_worker(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    worker_id = callback_data['worker_id']
    await call.message.delete()
    await state.update_data(worker_id=worker_id)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="first_name")))
    skip_btn.add(back_btn(menu=f"workerlist:{worker_id}"))
    await call.message.answer("Xodim ismini kiriting:", reply_markup=skip_btn)
    await EditWorker.first_name.set()


@dp.callback_query_handler(admin_filter, edit_worker_btn.filter(field="first_name"), state=EditWorker.first_name)
async def skip_first_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(first_name=None)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="last_name")))
    await call.message.answer("Familiya ni kiriting:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.message_handler(admin_filter, state=EditWorker.first_name)
async def edit_worker_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="last_name")))
    await message.answer("Familiya ni kiriting:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.callback_query_handler(admin_filter, edit_worker_btn.filter(field="last_name"), state=EditWorker.last_name)
async def skip_last_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(last_name=None)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="username")))
    await call.message.answer("Username ni kiriting:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.message_handler(admin_filter, state=EditWorker.last_name)
async def edit_worker_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="username")))
    await message.answer("Username ni kiriting:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.callback_query_handler(admin_filter, edit_worker_btn.filter(field="username"), state=EditWorker.username)
async def skip_username(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(username=None)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="password")))
    await call.message.answer("Parolni kiriting:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.message_handler(admin_filter, state=EditWorker.username)
async def edit_worker_username(message: types.Message, state: FSMContext):
    username = message.text
    await state.update_data(username=username)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="password")))
    await message.answer("Parolni kiriting:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.callback_query_handler(admin_filter, edit_worker_btn.filter(field="password"), state=EditWorker.password)
async def skip_password(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(password=None)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="photo")))
    await call.message.answer("Rasm yuboring:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.message_handler(admin_filter, state=EditWorker.password)
async def edit_worker_password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(password=password)
    skip_btn = types.InlineKeyboardMarkup()
    skip_btn.insert(
        types.InlineKeyboardButton(text="O'tkazib yuborish", callback_data=edit_worker_btn.new(field="photo")))
    await message.answer("Rasm yuboring:", reply_markup=skip_btn)
    await EditWorker.next()


@dp.callback_query_handler(admin_filter, edit_worker_btn.filter(field="photo"), state=EditWorker.photo)
async def skip_photo(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(photo=None)
    data = await state.get_data()
    worker_id = data.get("worker_id")
    if data.get("first_name"):
        first_name = data.get("first_name")
    else:
        first_name = (await db.select_user(id=int(worker_id)))['first_name']
    if data.get("last_name"):
        last_name = data.get("last_name")
    else:
        last_name = (await db.select_user(id=int(worker_id)))['last_name']
    if data.get("username"):
        username = data.get("username")
    else:
        username = (await db.select_user(id=int(worker_id)))['username']
    if data.get("password"):
        password = data.get("password")
    else:
        password = (await db.select_user(id=int(worker_id)))['password']
    if data.get("photo"):
        photo = data.get("photo")
    else:
        photo = (await db.select_user(id=int(worker_id)))['photo']
    await db.update_user(user_id=int(worker_id), first_name=first_name, last_name=last_name,
                         username=username,
                         password=password, photo=photo)
    msg = f"<b>Xodim o'zgartirildi:</b>\n\n" \
          f"<b>Ismi:</b> {first_name}\n" \
          f"<b>Familiyasi:</b> {last_name}\n" \
          f"<b>Username:</b> {username}\n"
    if photo:
        await call.message.answer_photo(photo, msg, parse_mode="HTML")
    else:
        await call.message.answer(msg, parse_mode="HTML")
    await state.finish()


@dp.message_handler(admin_filter, state=EditWorker.photo)
async def edit_worker_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Rasm yuboring!")
        return


@dp.message_handler(admin_filter, content_types=types.ContentType.PHOTO, state=EditWorker.photo)
async def edit_worker_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    worker_id = data.get("worker_id")
    if data.get("first_name"):
        first_name = data.get("first_name")
    else:
        first_name = (await db.select_user(id=int(worker_id)))['first_name']
    if data.get("last_name"):
        last_name = data.get("last_name")
    else:
        last_name = (await db.select_user(id=int(worker_id)))['last_name']
    if data.get("username"):
        username = data.get("username")
    else:
        username = (await db.select_user(id=int(worker_id)))['username']
    if data.get("password"):
        password = data.get("password")
    else:
        password = (await db.select_user(id=int(worker_id)))['password']
    if data.get("photo"):
        photo = data.get("photo")
    else:
        photo = (await db.select_user(id=int(worker_id)))['photo']
    await db.update_user(user_id=int(worker_id), first_name=first_name, last_name=last_name,
                         username=username, password=password, photo=photo)
    await message.answer("Xodim o'zgartirildi")
    await state.finish()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
