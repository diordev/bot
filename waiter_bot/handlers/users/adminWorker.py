from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.user_type import admin_filter
from keyboards.inline.workersList import add_worker_user_type
from states.addWorker import AddWorker
from loader import dp, db
from utils.check_password import validate_password


@dp.callback_query_handler(admin_filter, text_contains="addworker")
async def add_worker(call: types.CallbackQuery):
    await call.message.delete()
    user_types = add_worker_user_type
    await call.message.answer("Xodim turi:", reply_markup=user_types)
    await AddWorker.user_type.set()


@dp.callback_query_handler(admin_filter, state=AddWorker.user_type)
async def add_cashier(call: types.CallbackQuery, state: FSMContext):
    user_type = call.data.split(":")[-1]
    await call.message.delete()
    await call.message.answer("Ismni kiriting:")
    await state.update_data(user_type=user_type)
    await AddWorker.next()


@dp.message_handler(admin_filter, state=AddWorker.first_name)
async def add_cashier_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await message.answer("Familiya ni kiriting:")
    await AddWorker.next()


@dp.message_handler(admin_filter, state=AddWorker.last_name)
async def add_cashier_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await message.answer("Username ni kiriting:")
    await AddWorker.next()


@dp.message_handler(admin_filter, state=AddWorker.username)
async def add_cashier_username(message: types.Message, state: FSMContext):
    username = message.text
    user = await db.select_user(username=username)
    if user:
        await message.answer("Bunday username mavjud!")
        return
    await state.update_data(username=username)
    await message.answer("Parolni kiriting:")
    await AddWorker.next()


@dp.message_handler(admin_filter, state=AddWorker.password)
async def add_cashier_password(message: types.Message, state: FSMContext):
    password = message.text
    msg = validate_password(password)
    if msg:
        await message.answer(msg)
        return
    await state.update_data(password=password)
    await message.answer("Rasm yuboring:")
    await AddWorker.next()


@dp.message_handler(admin_filter, state=AddWorker.photo)
async def add_cashier_photo(message: types.Message):
    if not message.photo:
        await message.answer("Rasm yuboring!")
        return


@dp.message_handler(admin_filter, content_types=types.ContentType.PHOTO, state=AddWorker.photo)
async def add_cashier_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    password = data.get("password")
    user_type = data.get("user_type")
    company_id = (await db.select_user(telegram_id=message.from_user.id, auth_status=True))['company_id']
    await db.add_user(
        first_name=first_name,
        last_name=last_name,
        user_type=user_type,
        username=username,
        password=password,
        company_id=int(company_id),
        photo=photo,
        auth_status=False
    )
    match user_type:
        case "waiter":
            user_type = "Ofitsiant"
        case "cashier":
            user_type = "Kassir"
        case "cook":
            user_type = "Oshpaz"
    msg = f"<b>Yangi {user_type} qo'shildi!</b>\n\n" \
          f"<b>Ismi:</b> {first_name}\n" \
          f"<b>Familiyasi:</b> {last_name}\n" \
          f"<b>Username:</b> {username}\n"
    await message.answer_photo(photo, msg, parse_mode="HTML")
    await state.finish()
