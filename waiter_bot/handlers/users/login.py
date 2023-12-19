from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.adminKeyboards import worker
from keyboards.default.cashierKeyboards import cashier_actions
from keyboards.default.cookKeyboards import cook
from keyboards.default.waiterKeyboards import waiter_actions
from loader import dp, db
from states.login import Login
from keyboards.inline.login import login as login_btn


@dp.callback_query_handler(text="login")
async def login(call: types.CallbackQuery):
    await call.message.edit_text("Username kiriting:")
    await Login.username.set()


@dp.message_handler(state=Login.username)
async def login_username(message: types.Message, state: FSMContext):
    username = message.text
    user = await db.select_user(username=username)
    if not user:
        await message.answer("Bunday usernameli foydalanuvchi mavjud emas, qaytadan kiriting!")
        return
    await state.update_data(username=username)
    await message.answer("Parolni kiriting:")
    await Login.next()


@dp.message_handler(state=Login.password)
async def login_password(message: types.Message, state: FSMContext):
    password = message.text
    data = await state.get_data()
    username = data.get("username")
    user = await db.select_user(username=username)
    if user['password'] != password:
        await message.answer("Parol xato, qaytadan kiriting!")
        return
    if user:
        if user['telegram_id'] is not None:
            await message.answer("Bu akkauntga boshqa foydalanuvchi tizimga kirdi!")
            return
        await db.update_user(user['id'], auth_status=True, telegram_id=message.from_user.id)
        company = await db.select_company(id=user['company_id'])
        if company['is_active'] == 0:
            await message.answer("Sizning kompaniyangiz faol emas!")
            return
        msg = f"Assalomu alaykum {user['first_name']} !"
        match user['user_type']:
            case 'admin':
                await message.answer(msg, reply_markup=worker)
            case 'waiter':
                await message.answer(msg, reply_markup=waiter_actions)
            case 'cashier':
                await message.answer(msg, reply_markup=cashier_actions)
            case 'cook':
                await message.answer(msg, reply_markup=cook)
    else:
        await message.answer("Login yoki parol xato, qayta urinib ko'ring!", reply_markup=login_btn)
    await state.finish()
