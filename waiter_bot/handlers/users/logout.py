from aiogram import types
from loader import dp, db


@dp.message_handler(commands=['logout'], state="*")
async def logout(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id, auth_status=True)
    if user:
        await db.update_user(user['id'], auth_status=False, telegram_id=None)
        await message.answer("Siz tizimdan chiqdingiz!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Siz tizimga kirmagansiz!", reply_markup=types.ReplyKeyboardRemove())
