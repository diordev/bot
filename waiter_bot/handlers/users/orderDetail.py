from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.user_type import admin_or_waiter_filter
from keyboards.inline.addOrder import get_product_list
from keyboards.inline.orderDetail import get_order_detail
from loader import dp, db
from states.addOrder import Order


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="order:")
async def order_detail(call: types.CallbackQuery):
    table_id = int(call.data.split(":")[-1])
    table_name = (await db.select_table(id=table_id))['name']
    orders = await db.select_orders(table_id=table_id)
    msg = f"<b>Stol: {table_name}</b>\n"
    orders_dict = {}
    service_fee = 0
    for order in orders:
        product = await db.select_product(id=order['product_id'])
        product_name = product['name']
        quantity = order['weight']
        service_fee = int(order['service_fee']) / 100

        if product_name not in orders_dict:
            orders_dict[product_name] = 0

        orders_dict[product_name] += quantity
    total_price = 0
    for product_name, quantity in orders_dict.items():
        product = await db.select_product(name=product_name)
        unit = product['unit']
        price = product['price']
        total_price += float(quantity) * price
        if unit == "kg":
            quantity_ = f"{quantity} kg"
        else:
            quantity_ = f"{int(quantity)} ta"
        msg += f" <b>  {product_name}</b> - {quantity_} - <em>{int(price * float(quantity))} so'm</em>\n"
    msg += f"\n<b>Service fee: {service_fee * 100}% - {int(total_price * service_fee)} so'm</b>"
    total_price += total_price * service_fee
    msg += f"\n<b>Jami: {int(total_price)} so'm</b>"
    await call.message.delete()
    buttons = await get_order_detail(table_id=table_id)
    await call.message.answer(msg, parse_mode="HTML", reply_markup=buttons)
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="deleteOrder:")
async def delete_order(call: types.CallbackQuery):
    table_id = int(call.data.split(":")[-1])
    await db.delete_order(table_id=table_id)
    await db.update_table(table_id=table_id, is_active=False)
    await call.message.delete()
    await call.message.answer("Buyurtma o'chirildi!")
    await call.answer()


@dp.callback_query_handler(admin_or_waiter_filter, text_contains="updateOrder:")
async def update_order(call: types.CallbackQuery, state: FSMContext):
    table_id = int(call.data.split(":")[-1])
    company_id = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['company_id']
    await state.update_data(company_id=company_id, table_id=table_id)
    await call.message.delete()
    btn = await get_product_list(company_id=company_id)
    await call.message.answer("Mahsulot tanlang:", reply_markup=btn)
    await Order.product.set()
    await call.answer()
