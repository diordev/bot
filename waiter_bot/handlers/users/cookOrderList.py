from aiogram import types

from filters.user_type import cook_filter
from loader import dp, db


@dp.message_handler(cook_filter, text="Buyurtmalar")
async def cook_order_list(message: types.Message):
    orders = await db.select_orders(status="in_process")
    if orders:
        orders_dict = {}
        for order in orders:
            table = await db.select_table(id=order['table_id'])
            product = await db.select_product(id=order['product_id'])
            table_name = table['name']
            product_name = product['name']
            quantity = order['weight']

            if table_name not in orders_dict:
                orders_dict[table_name] = {}

            if product_name not in orders_dict[table_name]:
                orders_dict[table_name][product_name] = 0

            orders_dict[table_name][product_name] += quantity

        for table_name, products in orders_dict.items():
            msg = f"<b>Stol: {table_name}</b>\n"
            for product_name, quantity in products.items():
                unit = (await db.select_product(name=product_name))['unit']
                if unit == "kg":
                    quantity = f"{quantity} kg"
                else:
                    quantity = f"{int(quantity)} ta"
                msg += f" <b>  {product_name}</b> - {quantity}\n"
            table_id = (await db.select_table(name=table_name))['id']
            btn = types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Tayyor!", callback_data=f"cookorder:{table_id}"),
                ]
            ])
            await message.answer(msg, parse_mode="HTML", reply_markup=btn)
    else:
        await message.answer("Buyurtmalar yo'q)")