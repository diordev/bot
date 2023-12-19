from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from filters.user_type import admin_or_waiter_filter
from keyboards.inline.orderList import get_order_list, add_order_btn
from loader import dp, db


@dp.callback_query_handler(text="menuorder_list", state="*")
@dp.message_handler(admin_or_waiter_filter, text="Buyurtmalar", state="*")
async def order_list(message: types.Message, state: FSMContext):
    await state.finish()
    waiter = await db.select_user(telegram_id=message.from_user.id, auth_status=True)
    orders = await db.select_orders(company_id=waiter['company_id'], waiter_id=waiter['id'], status="in_process")
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
        message = message.message
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

        orders_list = "<b>Buyurtmalar:</b>\n\n"
        btn = await get_order_list(company_id=waiter['company_id'], waiter_id=waiter['id'])

        for table_name, products in orders_dict.items():
            orders_list += f"<b>Stol: {table_name}</b>\n"
            for product_name, quantity in products.items():
                unit = (await db.select_product(name=product_name))['unit']
                if unit == "kg":
                    quantity = f"{quantity} kg"
                else:
                    quantity = f"{int(quantity)} ta"
                orders_list += f" <b>  {product_name}</b> - {quantity}\n"

            orders_list += "\n"

        orders_list += "\n<b>Stol ni tanlang:</b>"
        await message.answer(orders_list, parse_mode="HTML", reply_markup=btn)
    else:
        btn = InlineKeyboardMarkup(inline_keyboard=[[add_order_btn]])
        await message.answer("Buyurtmalar mavjud emas!", reply_markup=btn)
