from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.user_type import admin_or_waiter_filter
from keyboards.inline.back import back_markup
from keyboards.inline.productDetail import choice_unit
from states.addProduct import Product
from loader import dp, db


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="addproduct")
@dp.callback_query_handler(state=Product.name)
async def add_product_category(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    category_id = int(call.data.split(":")[1])
    await state.update_data(category_id=category_id)
    await call.message.delete()
    back = back_markup(menu=f"catlist:{category_id}")
    await call.message.answer("Mahsulot nomini kiriting:", reply_markup=back)
    await Product.name.set()


@dp.message_handler(admin_or_waiter_filter, state=Product.name)
async def add_product_name(message: types.Message, state: FSMContext):
    name = message.text
    product = await db.select_product(name=name)
    if product:
        await message.answer("Bunday mahsulot mavjud!")
        return
    await state.update_data(name=name)
    await message.answer("Mahsulot o'lchov birligini kiriting:", reply_markup=choice_unit)
    await Product.unit.set()


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="unit", state=Product.unit)
async def add_product_unit(call: types.CallbackQuery, state: FSMContext):
    unit = call.data.split(":")[-1]
    await state.update_data(unit=unit)
    await call.message.delete()
    await call.message.answer("Mahsulot narxini kiriting:")
    await Product.next()


@dp.message_handler(admin_or_waiter_filter, state=Product.price)
async def add_product_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("Narxni raqamda kiriting!")
        return
    await state.update_data(price=price)
    await message.answer("Mahsulot haqida qo'shimcha malumot kiriting:")
    await Product.next()


@dp.message_handler(admin_or_waiter_filter, state=Product.description)
async def add_product_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("Mahsulot rasmini yuboring:")
    await Product.next()


@dp.message_handler(admin_or_waiter_filter, state=Product.photo)
async def add_product_photo(message: types.Message):
    if not message.photo:
        await message.answer("Rasm yuboring!")
        return


@dp.message_handler(admin_or_waiter_filter, content_types=types.ContentType.PHOTO, state=Product.photo)
async def add_product_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    category_id = data.get("category_id")
    name = data.get("name")
    unit = data.get("unit")
    price = data.get("price")
    description = data.get("description")
    company_id = (await db.select_user(telegram_id=message.from_user.id, auth_status=True))['company_id']
    await db.add_product(
        name=name,
        unit=unit,
        price=int(price),
        photo=photo,
        category_id=int(category_id),
        company_id=int(company_id),
        description=description
    )
    await message.answer("Mahsulot qo'shildi!")
    await state.finish()
