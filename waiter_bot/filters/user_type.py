from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import db, dp


class UserTypeFilter(BoundFilter):
    key = 'user_type'

    def __init__(self, user_type):
        self.user_type = user_type

    async def company_check(self, user, message: types.Message):
        company = await db.select_company(id=user['company_id'])
        if company['is_active'] == 0:
            await message.answer("Sizning kompaniyangiz faol emas!")
            return False
        return True

    async def check(self, message: types.Message):
        user = await db.select_user(telegram_id=message.from_user.id)
        if user:
            company = await self.company_check(user, message)
            if company:
                return user['user_type'] == self.user_type
            return False
        return False


class AdminWaiterCheckFilter(UserTypeFilter):
    key = 'admin_waiter_check'

    def __init__(self, type2, user_type):
        super().__init__(user_type)
        self.type2 = type2

    async def check(self, message: types.Message):
        user = await db.select_user(telegram_id=message.from_user.id)
        if user:
            company = await self.company_check(user, message)
            if company:
                return user['user_type'] == self.user_type or user['user_type'] == self.type2
            return False
        return False


waiter_filter = UserTypeFilter("waiter")
cashier_filter = UserTypeFilter("cashier")
admin_filter = UserTypeFilter("admin")
cook_filter = UserTypeFilter("cook")
admin_or_waiter_filter = AdminWaiterCheckFilter("admin", "waiter")

dp.filters_factory.bind(UserTypeFilter, event_handlers=[dp.message_handlers])