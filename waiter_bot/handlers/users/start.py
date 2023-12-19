from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.adminKeyboards import worker
from keyboards.default.cashierKeyboards import cashier_actions
from keyboards.default.cookKeyboards import cook
from keyboards.default.waiterKeyboards import waiter_actions
from keyboards.inline.login import login
from loader import dp, db


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    user = await db.select_user(telegram_id=message.from_user.id, auth_status=True)
    if not user:
        await message.answer("Bot ga kirish uchun <em>Login</em> tugmasini bosing:",
                             reply_markup=login, parse_mode="HTML")
    else:
        company = await db.select_company(id=user['company_id'])
        if company['is_active'] == 0:
            await message.answer("Sizning kompaniyangiz faol emas!")
            return
        answer = f"Assalomu alaykum {user['first_name']}!"
        match user['user_type']:
            case "admin":
                answer += "\n\n<b>Admin paneliga xush kelibsiz!</b>"
                await message.answer(answer, reply_markup=worker, parse_mode="HTML")
            case "waiter":
                answer += "\n\n<b>Waiter paneliga xush kelibsiz!</b>"
                await message.answer(answer, reply_markup=waiter_actions, parse_mode="HTML")
            case "cook":
                answer += "\n\n<b>Oshpaz paneliga xush kelibsiz!</b>"
                await message.answer(answer, reply_markup=cook, parse_mode="HTML")
            case "cashier":
                answer += "\n\n<b>Kassir paneliga xush kelibsiz!</b>"
                await message.answer(answer, reply_markup=cashier_actions, parse_mode="HTML")
            case _:
                await message.answer("Sizning huquqingiz yo'q!")
