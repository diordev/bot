from aiogram import types

from filters.user_type import cashier_filter
from keyboards.inline.back import back_btn
from loader import dp, db


@dp.callback_query_handler(cashier_filter, text_contains="table_order:")
async def table_order(call: types.CallbackQuery):
    table_id = int(call.data.split(":")[-1])
    table = await db.select_table(id=table_id)
    orders = await db.select_orders(table_id=table_id)
    msg = f"<b>Stol: {table['name']}</b>\n"
    service_fee = 0
    orders_dict = {}
    for order in orders:
        product = await db.select_product(id=order['product_id'])
        product_name = product['name']
        quantity = order['weight']
        price = product['price']
        service_fee = int(order['service_fee']) / 100

        if product_name not in orders_dict:
            orders_dict[product_name] = {'quantity': 0, 'price': price}

        orders_dict[product_name]['quantity'] += quantity

    total_price = 0
    for product_name, data in orders_dict.items():
        msg += f" <b>  {product_name}</b> - <em>{data['price']} so'm</em> X {data['quantity']}\n"
        total_price += float(data['quantity']) * data['price']

    msg += f"\n<b>Service fee: {service_fee * 100}% - {int(total_price * service_fee)} so'm</b>"
    total_price += total_price * service_fee
    msg += f"\n<b>Jami: {total_price} so'm</b>"
    await call.message.delete()
    btn = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Submit", callback_data=f"pay:{table_id}"),
        ],
        [back_btn(menu="menucashiertable_list")]
    ])
    await call.message.answer(msg, parse_mode="HTML", reply_markup=btn)
    await call.answer()


@dp.callback_query_handler(cashier_filter, text_contains="pay:")
async def pay(call: types.CallbackQuery):
    table_id = int(call.data.split(":")[-1])
    await db.update_order_with_table_id(table_id=table_id, status="payed")
    await db.update_table(table_id=table_id, is_active=False)
    await call.message.delete()
    await call.message.answer("Buyurtma yakunlandi!")
    await call.answer()
