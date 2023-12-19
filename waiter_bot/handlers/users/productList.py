from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from filters.user_type import admin_or_waiter_filter
from keyboards.inline.back import back_btn
from keyboards.inline.productCat import get_categories_list
from keyboards.inline.productList import get_products_list, add_product_btn
from loader import dp, db
from states.addProduct import Product


@dp.callback_query_handler(text="menucategory_list")
@dp.message_handler(admin_or_waiter_filter, text="Mahsulotlar", state="*")
async def category_list(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    await state.finish()
    company_id = (await db.select_user(telegram_id=message.from_user.id, auth_status=True))['company_id']
    categories = await db.select_categories(company_id=company_id)
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
        message = message.message
    if categories:
        buttons = await get_categories_list(company_id=company_id)
        await message.answer("Kategoriyani tanlang:", reply_markup=buttons)
    else:
        await message.answer("Kategoriyalar mavjud emas!")


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="catlist:")
@dp.callback_query_handler(state=Product.name)
async def category_list(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    await state.finish()
    category_id = int(call.data.split(":")[1])
    company_id = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['company_id']
    products = await db.select_products(category_id=category_id)
    back = back_btn(menu='menucategory_list')
    if products:
        category_name = (await db.select_category(id=category_id))['name']
        products_list = f'<b><em>"{category_name}"</em>  kategoriyasining mahsulotlari:</b>\n\n'
        buttons = await get_products_list(company_id=company_id, category_id=category_id)
        buttons.row(back)
        await call.message.delete()
        await call.message.answer(products_list, parse_mode="HTML", reply_markup=buttons)
    else:
        add_product_btn.callback_data = f"addproduct:{category_id}"
        btn = InlineKeyboardMarkup(inline_keyboard=[[add_product_btn, back]])
        await call.message.delete()
        await call.message.answer("Bu kategoriyada mahsulotlar mavjud emas!", reply_markup=btn)
    await call.answer()
