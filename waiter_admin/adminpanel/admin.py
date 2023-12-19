from django.contrib import admin

from .models import UserModel, ProductModel, CategoryModel, TableModel, CompanyModel, OrderModel, PaymentModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(TableModel)
admin.site.register(CompanyModel)
admin.site.register(OrderModel)
admin.site.register(PaymentModel)
