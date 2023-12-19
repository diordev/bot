from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime
from filters.user_type import cook_filter, admin_or_waiter_filter
from keyboards.inline.addOrder import (get_empty_table_list, get_product_list, get_product_quantity, add_order_keyboard,
                                       service_charge_keyboard, get_confirm_keyboard, get_cook_keyboard)
from keyboards.inline.back import back_btn, back_markup
from keyboards.inline.addOrder import get_product_unit
from loader import dp, db, bot
from states.addOrder import Order
from utils.send_photo import product_photo


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="add_order")
async def add_order(call: types.CallbackQuery, state: FSMContext):
    company_id = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['company_id']
    await state.update_data(company_id=company_id)
    empty_table_list = await get_empty_table_list(company_id=company_id)
    back = back_btn(menu="menuorder_list")
    await call.message.delete()
    if empty_table_list['inline_keyboard']:
        await call.message.answer("Stolni tanlang:", reply_markup=empty_table_list.row(back))
        await Order.table.set()
    else:
        back = back_markup(menu="menuorder_list")
        await call.message.answer("Bo'sh stollar mavjud emas!", reply_markup=back)
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, state=Order.table)
@dp.callback_query_handler(admin_or_waiter_filter, text_contains="add_new_product", state=Order.quantity)
async def add_order(call: types.CallbackQuery, state: FSMContext):
    if call.data != "add_new_product":
        table_id = int(call.data.split(":")[-1])
        await state.update_data(table_id=table_id)
    company_id = (await state.get_data())['company_id']
    product_list = await get_product_list(company_id=company_id)
    await call.message.delete()
    await call.message.answer("Mahsulot tanlang:", reply_markup=product_list)
    await Order.product.set()
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, state=Order.product)
async def add_order(call: types.CallbackQuery, state: FSMContext):
    product_id = int(call.data.split(":")[-1])
    products = (await state.get_data()).get('products', {})
    if products:
        products[product_id] = 1
        await state.update_data(products=products)
    else:
        await state.update_data(products={product_id: 1})
    product = await db.select_product(id=product_id)
    await call.message.delete()
    if product['unit'] == "kg":
        buttons = await get_product_unit(product_id=product_id)
        await call.message.answer("Gram da yoki kilogramm da buyurtma qlasizmi?", reply_markup=buttons)
        await call.answer()
        await Order.unit.set()
        return
    msg = f"<b>{product['name']}</b>\n\n"
    msg += f"Narxi: {product['price']}\n"
    msg += f"{product['description']}\n\n"
    photo = product['photo']
    quantity = await state.update_data(quantity=1)
    buttons = await get_product_quantity(product_id=product_id, quantity=quantity)
    if photo:
        photo = await product_photo(photo=photo)
        await call.message.answer_photo(photo=photo, caption=msg, reply_markup=buttons)
    else:
        await call.message.answer(msg, reply_markup=buttons)
    await Order.quantity.set()
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="unit", state=Order.unit)
async def add_order(call: types.CallbackQuery, state: FSMContext):
    product_id = int(call.data.split(":")[0])
    unit = call.data.split(":")[-1]
    await state.update_data(unit=unit)
    await state.update_data(product_id=product_id)
    await call.message.delete()
    product = await db.select_product(id=product_id)
    msg = f"<b>{product['name']}</b>\n\n"
    msg += f"Narxi: {product['price']}\n"
    msg += f"{product['description']}\n\n"
    photo = product['photo']
    if photo:
        photo = await product_photo(photo=photo)
        await call.message.answer_photo(photo=photo, caption=msg)
    else:
        await call.message.answer(msg)
    if unit == "kg":
        await call.message.answer("Bu mahsulotdan necha kilogramm buyurtma qilasiz?")
    elif unit == "gram":
        await call.message.answer("Bu mahsulotdan necha gram buyurtma qilasiz?")
    await Order.quantity.set()
    await call.answer()


@dp.message_handler(admin_or_waiter_filter, state=Order.quantity)
async def add_order(message: types.Message, state: FSMContext):
    unit = (await state.get_data())['unit']
    product_id = (await state.get_data())['product_id']
    products = (await state.get_data())['products']
    quantity = message.text
    if not quantity.isdigit():
        await message.answer("Son kiriting, iltimos!")
        return
    if unit == "gram":
        quantity = int(quantity) / 1000
    await state.update_data(quantity=quantity)
    await message.delete()
    products[product_id] = quantity
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 2)
    await message.answer("Mahsulot qo'shildi", reply_markup=add_order_keyboard)
    await state.update_data(products=products)


@dp.callback_query_handler(admin_or_waiter_filter, state=Order.quantity, text_contains="addOrderQuantity")
async def order_quantity(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    product_id = int(call.data.split(":")[0])
    products = (await state.get_data())['products']
    quantity = products[product_id]
    action = call.data.split(":")[-1]
    await call.answer()
    if action == "Submit":
        await call.message.delete()
        products[product_id] = quantity
        await call.message.answer("Mahsulot qo'shildi", reply_markup=add_order_keyboard)
        await state.update_data(products=products)
        return
    elif action == "+":
        quantity += 1
    elif action == "-":
        if quantity > 1:
            quantity -= 1
        else:
            await call.answer("Soni 1 dan kam bo'lishi mumkin emas!")
            return
    products[product_id] = quantity
    await state.update_data(products=products)
    buttons = await get_product_quantity(product_id=product_id, quantity=quantity)
    await call.message.edit_reply_markup(buttons)


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="finish_order", state=Order.quantity)
async def finish_order(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Xizmat xaqi foizi:", reply_markup=service_charge_keyboard)
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="service_charge", state=Order.quantity)
async def service_charge(call: types.CallbackQuery, state: FSMContext):
    service_fee = int(call.data.split(":")[-1])
    data = await state.get_data()
    products = data['products']
    table_id = int(data['table_id'])
    company_id = data['company_id']
    waiter = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['id']
    msg = f"<b>Stol: {(await db.select_table(id=table_id))['name']}</b>\n"
    total_price = 0

    for product_id, quantity in products.items():
        await db.create_new_order(table_id=table_id, product_id=product_id, weight=quantity, waiter_id=waiter,
                                  company_id=company_id, status="new", service_fee=service_fee)
        product = await db.select_product(id=product_id)
        if product['unit'] == "kg":
            weight = f"{quantity} kg"
        else:
            weight = f"{int(quantity)} ta"
        msg += f" <b>  {product['name']}</b> - {weight} - {product['price'] * quantity} so'm\n"
        total_price += product['price'] * quantity
    await db.update_table(table_id=table_id, is_active=True)
    await call.message.delete()
    buttons = await get_confirm_keyboard(table_id=table_id)
    msg += f"\n<b>Summa:</b> {total_price} so'm"
    msg += f"\n<b>Xizmat xaqi:</b> {service_fee}% - {int(total_price * service_fee / 100)} so'm"
    msg += f"\n<b>Jami:</b> {int(total_price + total_price * service_fee / 100)} so'm"
    msg += "\n\n<b>Buyurtmani tasdiqlaysizmi:</b>"
    await call.message.answer(msg, reply_markup=buttons)
    await state.finish()
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="order_confirm")
async def confirm_order(call: types.CallbackQuery):
    table_id = int(call.data.split(":")[-1])
    now = datetime.now()
    await db.update_order_with_table_id(table_id=table_id, status="in_process", created_at=now)
    await call.message.delete()
    await call.message.answer("Buyurtma qabul qilindi!")
    await call.answer()
    cooks = await db.select_cooks()
    for cook in cooks:
        if cook['is_active'] == 0 or cook['telegram_id'] is None:
            continue
        table_name = (await db.select_table(id=table_id))['name']
        msg = f"<b>Stol: {table_name}</b>\n"
        orders = await db.select_orders(table_id=table_id)
        orders_dict = {}
        for order in orders:
            product = await db.select_product(id=order['product_id'])
            product_name = product['name']
            quantity = order['weight']

            if product_name not in orders_dict:
                orders_dict[product_name] = 0

            orders_dict[product_name] += quantity
        for product_name, quantity in orders_dict.items():
            unit = (await db.select_product(name=product_name))['unit']
            if unit == "kg":
                quantity = f"{quantity} kg"
            else:
                quantity = f"{int(quantity)} ta"
            msg += f" <b>  {product_name}</b> - {quantity}\n"
        button = await get_cook_keyboard(table_id=table_id)
        await dp.bot.send_message(chat_id=cook['telegram_id'], text=msg, parse_mode="HTML", reply_markup=button)


@dp.callback_query_handler(cook_filter, text_contains="cookorder:")
async def cook_order(call: types.CallbackQuery):
    table_id = int(call.data.split(":")[-1])
    await db.update_order_with_table_id(table_id=table_id, status="done")
    await db.update_table(table_id=table_id, is_active=False)
    await call.message.delete()
    await call.answer("Buyurtma tayyorlandi!")
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="order_cancel")
async def cancel_order(call: types.CallbackQuery):
    table_id = int(call.data.split(":")[-1])
    await db.delete_order(table_id=table_id)
    await call.message.delete()
    await call.message.answer("Buyurtma bekor qilindi!")
    await call.answer()
