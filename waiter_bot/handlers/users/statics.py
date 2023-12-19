from aiogram import types
from datetime import datetime, timedelta
from filters.user_type import admin_filter
from keyboards.inline.waiterList import get_waiter_list
from loader import dp, db
from utils.statistics import write_general_statistics_excel, write_by_waiter_statistics_excel, \
    write_by_product_statistics_excel


@dp.message_handler(admin_filter, text="Statistika")
async def statistics(message: types.Message):
    btn = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kunlik", callback_data="daily_statistics"),
                types.InlineKeyboardButton(text="Haftalik", callback_data="weekly_statistics"),
                types.InlineKeyboardButton(text="Oylik", callback_data="monthly_statistics"),
                types.InlineKeyboardButton(text="Yillik", callback_data="all_statistics")
            ]
        ])
    await message.answer("Statistika turi:", reply_markup=btn)


@dp.callback_query_handler(admin_filter, text_contains="statistics")
async def statistics(call: types.CallbackQuery):
    date_range = call.data.split("_")[0]
    btn = types.InlineKeyboardMarkup(row_width=1)
    btn.add(types.InlineKeyboardButton(text="Umumiy statistika", callback_data=f"{date_range}_general"))
    btn.add(types.InlineKeyboardButton(text="Ofitsiantlar statistikasi", callback_data=f"{date_range}_waiters"))
    btn.add(types.InlineKeyboardButton(text="Mahsulotlar statistikasi", callback_data=f"{date_range}_products"))
    await call.message.edit_text("Statistika turi:", reply_markup=btn)


@dp.callback_query_handler(admin_filter, text_contains="general")
async def statistics(call: types.CallbackQuery):
    date_range = call.data.split("_")[0]
    start_date = None
    photo = "pics/general/"
    if date_range == "daily":
        start_date = datetime.now() - timedelta(days=1)
        photo = photo + "Kunlik.png"
    elif date_range == "weekly":
        start_date = datetime.now() - timedelta(days=7)
        photo = photo + "Haftalik.png"
    elif date_range == "monthly":
        start_date = datetime.now() - timedelta(days=30)
        photo = photo + "Oylik.png"
    elif date_range == "all":
        start_date = datetime.now() - timedelta(days=365)
        photo = photo + "Yillik.png"
    photo = types.InputFile(photo)
    company_id = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['company_id']
    best_selling_product = (await db.best_selling_product(company_id=company_id, date_from=start_date))[0]
    order_count = (await db.order_count(company_id=company_id, date_from=start_date))['total_orders']
    total_price = (await db.total_price(company_id=company_id, date_from=start_date))['total_price']
    service_fee = (await db.total_service_fee(company_id=company_id, date_from=start_date))['total_service_fee']
    queryset = await db.get_statistics(company_id=company_id, date_from=start_date)
    await call.message.delete()
    await call.answer()
    if best_selling_product and order_count and total_price and service_fee and queryset:
        general_statistics = {
            'total_orders': order_count,
            'total_price': total_price,
            'service_fee': service_fee,
            'total': total_price + service_fee
        }
        file = await write_general_statistics_excel(chat_id=call.from_user.id,
                                                    best_selling_product=best_selling_product,
                                                    general_statistics=general_statistics,
                                                    queryset=queryset)
        msg = "<em><b>Eng ko'p sotilgan mahsulot</b></em>\n"
        msg += f"{best_selling_product['name'].capitalize()} - "
        product = await db.select_product(name=best_selling_product['name'])
        if product['unit'] == "kg":
            msg += f"{best_selling_product['total_weight']} kg"
        else:
            msg += f"{int(best_selling_product['total_weight'])} dona"
        msg += f" - {int(best_selling_product['total_price'])} so'm\n\n\n"
        msg += "<em><b>Umumiy statistika</b></em>\n"
        msg += f"<b>Buyurtmalar soni - </b> {int(general_statistics['total_orders'])}\n"
        msg += f"<b>Jami sotuv - </b>{int(general_statistics['total_price'])} so'm\n"
        msg += f"<b>Xizmatlar summasi - </b>{int(general_statistics['service_fee'])} so'm\n"
        msg += f"<b>Jami summa - </b>{int(general_statistics['total'])} so'm"
        await call.message.answer_photo(photo=photo, caption=msg, parse_mode="HTML")
        await call.message.answer_document(document=file)
        file.close()
    else:
        await call.message.answer("Statistika mavjud emas!")


@dp.callback_query_handler(admin_filter, text_contains="waiters")
async def statistics(call: types.CallbackQuery):
    date_range = call.data.split("_")[0]
    company_id = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['company_id']
    waiter_list = await get_waiter_list(company_id=company_id, date_range=date_range)
    await call.message.delete()
    await call.answer()
    if waiter_list.inline_keyboard:
        await call.message.answer("Ofitsiantni tanlang:", reply_markup=waiter_list)
    else:
        await call.message.answer("Ofitsiantlar mavjud emas!")


@dp.callback_query_handler(admin_filter, text_contains="waiter")
async def statistics(call: types.CallbackQuery):
    date_range = call.data.split("_")[0]
    waiter_id = int(call.data.split("_")[-1])
    start_date = None
    photo = "pics/waiters/"
    if date_range == "daily":
        start_date = datetime.now() - timedelta(days=1)
        photo = photo + "Kunlik.png"
    elif date_range == "weekly":
        start_date = datetime.now() - timedelta(days=7)
        photo = photo + "Haftalik.png"
    elif date_range == "monthly":
        start_date = datetime.now() - timedelta(days=30)
        photo = photo + "Oylik.png"
    elif date_range == "all":
        start_date = datetime.now() - timedelta(days=365)
        photo = photo + "Yillik.png"
    photo = types.InputFile(photo)
    company_id = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['company_id']
    print(company_id)
    order_count = \
        (await db.get_order_count_by_waiter(company_id=company_id, waiter_id=waiter_id, date_from=start_date))[
            'total_orders']
    total_price = (await db.total_price_by_waiter(company_id=company_id, waiter_id=waiter_id, date_from=start_date))[
        'total_price']
    service_fee = \
        (await db.total_service_fee_by_waiter(company_id=company_id, waiter_id=waiter_id, date_from=start_date))[
            'total_service_fee']
    waiter = await db.select_user(id=waiter_id)
    await call.message.delete()
    await call.answer()
    if order_count and total_price and service_fee:
        queryset = {
            'waiter': waiter['first_name'] + " " + waiter['last_name'],
            'total_orders': order_count,
            'total_price': total_price,
            'service_fee': service_fee,
            'total': total_price + service_fee
        }
        file = await write_by_waiter_statistics_excel(queryset=queryset, chat_id=call.from_user.id)
        msg = "<em><b>Ofitsiant statistikasi</b></em>\n"
        msg += f"<b>Ofitsiant - </b> {queryset['waiter'].title()}\n"
        msg += f"<b>Buyurtmalar soni - </b> {int(queryset['total_orders'])}\n"
        msg += f"<b>Jami sotuv - </b>{int(queryset['total_price'])} so'm\n"
        msg += f"<b>Xizmatlar summasi - </b>{int(queryset['service_fee'])} so'm\n"
        msg += f"<b>Jami summa - </b>{int(queryset['total'])} so'm"
        await call.message.answer_photo(photo=photo, caption=msg, parse_mode="HTML")
        await call.message.answer_document(document=file)
    else:
        await call.message.answer("Statistika mavjud emas!")


@dp.callback_query_handler(admin_filter, text_contains="products")
async def statistics(call: types.CallbackQuery):
    date_range = call.data.split("_")[0]
    start_date = None
    photo = "pics/products/"
    if date_range == "daily":
        start_date = datetime.now() - timedelta(days=1)
        photo = photo + "Kunlik.png"
    elif date_range == "weekly":
        start_date = datetime.now() - timedelta(days=7)
        photo = photo + "Haftalik.png"
    elif date_range == "monthly":
        start_date = datetime.now() - timedelta(days=30)
        photo = photo + "Oylik.png"
    elif date_range == "all":
        start_date = datetime.now() - timedelta(days=365)
        photo = photo + "Yillik.png"
    photo = types.InputFile(photo)
    company_id = (await db.select_user(telegram_id=call.from_user.id, auth_status=True))['company_id']
    queryset = await db.get_statistics_by_products(company_id=company_id, date_from=start_date)
    await call.message.delete()
    await call.answer()
    if queryset:
        file = await write_by_product_statistics_excel(queryset=queryset, chat_id=call.from_user.id)
        msg = "<em><b>Mahsulotlar statistikasi</b></em>\n"
        for i in queryset:
            product = await db.select_product(name=i['product_name'])
            if product['unit'] == "kg":
                msg += f"<b>{i['product_name'].capitalize()} - </b> {i['total_weight']} kg - {int(i['total_price'])} so'm\n"
            else:
                msg += f"<b>{i['product_name'].capitalize()} - </b> {int(i['total_weight'])} dona - {int(i['total_price'])} so'm\n"
        await call.message.answer_photo(photo=photo, caption=msg, parse_mode="HTML")
        await call.message.answer_document(document=file)
    else:
        await call.message.answer("Statistika mavjud emas!")
