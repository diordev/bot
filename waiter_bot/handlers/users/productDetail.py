from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.user_type import admin_or_waiter_filter
from keyboards.inline.productDetail import product_detail_btn, edit_product_btn, get_product_detail_keyboard, \
    get_edit_product_keyboard, get_edit_skip_btn
from loader import dp, db
from states.addProduct import EditProduct
from utils.send_photo import product_photo


@dp.callback_query_handler(admin_or_waiter_filter, lambda x: x.data.startswith("productlist:"))
@dp.callback_query_handler(lambda x: x.data.startswith("productlist:"), state=EditProduct.name)
async def show_product_detail(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    print(call.data)
    product_id = int(call.data.split(":")[1])
    product = await db.select_product(id=product_id)
    photo = product['photo']
    unit = product['unit']
    product_detail = f"<b><em>{product['name']}</em></b>\n\n"
    if unit == "kg":
        product_detail += f"<b>Narxi:</b> {product['price']} <em>so'm/kg</em>\n"
    else:
        product_detail += f"<b>Narxi:</b> {product['price']} <em>so'm</em>\n"
    buttons = await get_product_detail_keyboard(product_id=product_id, category_id=product['category_id'])
    if product['description']:
        product_detail += f"<em>{product['description']}</em>"
    if photo:
        photo = await product_photo(photo)
        await call.message.delete()
        await call.message.answer_photo(photo, product_detail, parse_mode="HTML", reply_markup=buttons)
    else:
        await call.message.delete()
        await call.message.answer(product_detail, parse_mode="HTML", reply_markup=buttons)
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, product_detail_btn.filter(action="del"))
async def delete_product(call: types.CallbackQuery, callback_data: dict):
    product_id = int(callback_data['product_id'])
    await db.delete_product(id=product_id)
    await call.message.delete()
    await call.message.answer("Mahsulot o'chirildi")
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, product_detail_btn.filter(action="update"))
@dp.callback_query_handler(product_detail_btn.filter(action="update"), state=EditProduct.name)
async def update_product(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    product_id = int(callback_data['product_id'])
    await call.message.delete()
    await state.update_data(product_id=product_id)
    skip_btn = await get_edit_product_keyboard(product_id=product_id)
    await call.message.answer("Yangi mahsulot nomini kiriting:", reply_markup=skip_btn)
    await EditProduct.name.set()


@dp.message_handler(admin_or_waiter_filter, state=EditProduct.name)
async def update_product_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    skip_btn = await get_edit_skip_btn(field="price")
    await message.answer("Yangi mahsulot narxini kiriting:", reply_markup=skip_btn)
    await EditProduct.next()


@dp.callback_query_handler(admin_or_waiter_filter, edit_product_btn.filter(field="name"), state=EditProduct.name)
async def skip_update_product_name(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(name=None)
    skip_btn = await get_edit_skip_btn(field="price")
    await call.message.delete()
    await call.message.answer("Yangi mahsulot narxini kiriting:", reply_markup=skip_btn)
    await EditProduct.next()


@dp.message_handler(admin_or_waiter_filter, state=EditProduct.price)
async def update_product_price(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    skip_btn = await get_edit_skip_btn(field="description")
    await message.answer("Yangi mahsulot haqida qo'shimcha malumot kiriting:", reply_markup=skip_btn)
    await EditProduct.next()


@dp.callback_query_handler(admin_or_waiter_filter, edit_product_btn.filter(field="price"), state=EditProduct.price)
async def skip_update_product_price(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(price=None)
    skip_btn = await get_edit_skip_btn(field="description")
    await call.message.delete()
    await call.message.answer("Yangi mahsulot haqida qo'shimcha malumot kiriting:", reply_markup=skip_btn)
    await EditProduct.next()


@dp.message_handler(admin_or_waiter_filter, state=EditProduct.description)
async def update_product_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    skip_btn = await get_edit_skip_btn(field="photo")
    await message.answer("Yangi mahsulot rasmini yuboring:", reply_markup=skip_btn)
    await EditProduct.next()


@dp.callback_query_handler(admin_or_waiter_filter, edit_product_btn.filter(field="description"), state=EditProduct.description)
async def skip_update_product_description(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(description=None)
    skip_btn = await get_edit_skip_btn(field="photo")
    await call.message.delete()
    await call.message.answer("Yangi mahsulot rasmini yuboring:", reply_markup=skip_btn)
    await EditProduct.next()


@dp.message_handler(admin_or_waiter_filter, state=EditProduct.photo)
async def update_product_photo(message: types.Message):
    if not message.photo:
        await message.answer("Rasm yuboring!")
        return


@dp.message_handler(admin_or_waiter_filter, content_types=types.ContentType.PHOTO, state=EditProduct.photo)
async def update_product_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    product_id = data.get("product_id")
    if data.get('name'):
        name = data.get('name')
    else:
        name = (await db.select_product(id=int(product_id)))['name']
    if data.get('price'):
        price = data.get('price')
    else:
        price = (await db.select_product(id=int(product_id)))['price']
    if data.get('description'):
        description = data.get('description')
    else:
        description = (await db.select_product(id=int(product_id)))['description']

    await db.update_product(
        product_id=product_id,
        name=name,
        price=int(price),
        photo=photo,
        description=description
    )
    await state.finish()
    await message.answer("Mahsulot yangilandi")


@dp.callback_query_handler(admin_or_waiter_filter, edit_product_btn.filter(field="photo"), state=EditProduct.photo)
async def skip_update_product_photo(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    if data.get('name'):
        name = data.get('name')
    else:
        name = (await db.select_product(id=int(product_id)))['name']
    if data.get('price'):
        price = data.get('price')
    else:
        price = (await db.select_product(id=int(product_id)))['price']
    if data.get('description'):
        description = data.get('description')
    else:
        description = (await db.select_product(id=int(product_id)))['description']
    await db.update_product(
        product_id=product_id,
        name=name,
        price=int(price),
        description=description
    )
    await state.finish()
    await call.message.delete()
    await call.message.answer("Mahsulot yangilandi")
