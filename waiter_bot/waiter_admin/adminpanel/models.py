from django.db import models
import uuid

# Create your models here.
USER_TYPES = (
    ('super_admin', 'SuperAdmin'),
    ('admin', 'Admin'),
    ('waiter', 'Waiter'),
    ('cashier', 'Cashier'),
    ('cook', 'Cook'),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True


class CompanyModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    address = models.CharField(max_length=255, verbose_name="Address")
    phone = models.CharField(max_length=255, verbose_name="Phone number")
    is_active = models.BooleanField(default=False, verbose_name="Is active")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "companies"


class PaymentModel(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, verbose_name="Company", related_name="payments")
    amount = models.PositiveBigIntegerField(verbose_name="Amount")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.company} - {self.amount}"

    def save(self, *args, **kwargs):
        company = self.company
        company.is_active = True
        company.save()
        super(PaymentModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        company = self.company
        company.is_active = False
        company.save()
        super(PaymentModel, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payments"


class UserModel(BaseModel):
    first_name = models.CharField(max_length=255, verbose_name="First name")
    last_name = models.CharField(max_length=255, verbose_name="Last name", null=True, blank=True)
    user_type = models.CharField(max_length=255, verbose_name="User type", choices=USER_TYPES, default='waiter')
    username = models.CharField(max_length=255, verbose_name="Username", unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, verbose_name="Password")
    telegram_id = models.PositiveBigIntegerField(verbose_name="Telegram ID", null=True, blank=True)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, verbose_name="Company", related_name="users")
    photo = models.ImageField(upload_to='users/', verbose_name="Photo", null=True, blank=True)
    auth_status = models.BooleanField(default=False, verbose_name="Auth status")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.last_name is None:
            self.last_name = ""
        super(UserModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"


class TableModel(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, verbose_name="Company", related_name="tables")
    is_active = models.BooleanField(default=False, verbose_name="Is active")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        db_table = "tables"


class CategoryModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, verbose_name="Company",
                                related_name="categories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"


UNIT_CHOICES = (
    ('piece', 'Piece'),
    ('kg', 'Kilogram'),
)


class ProductModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    price = models.PositiveBigIntegerField(verbose_name="Price")
    photo = models.ImageField(upload_to='products/', verbose_name="Photo", null=True, blank=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name="Category",
                                 related_name="products")
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, verbose_name="Company", related_name="products")
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    unit = models.CharField(max_length=255, verbose_name="Unit", choices=UNIT_CHOICES, default='piece')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"


ORDER_STATUS = (
    ('new', 'New'),
    ('in_process', 'In process'),
    ('payed', 'Payed'),
    ('done', 'Done'),
)

SERVICE_FEE_CHOICES = (
    (0, '0%'),
    (5, '5%'),
    (10, '10%'),
    (15, '15%'),
    (20, '20%'),
)


class OrderModel(BaseModel):
    table = models.ForeignKey(TableModel, on_delete=models.CASCADE, verbose_name="Table", related_name="orders")
    waiter = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="Waiter", related_name="orders")
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, verbose_name="Company", related_name="orders")
    status = models.CharField(max_length=255, verbose_name="Status", choices=ORDER_STATUS, default='new')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name="Product", related_name="orders")
    service_fee = models.PositiveSmallIntegerField(
        choices=SERVICE_FEE_CHOICES,
        verbose_name="Service Fee",
        default=0
    )
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Weight")

    def __str__(self):
        return f"{self.table} - {self.waiter}"

    def save(self, *args, **kwargs):
        table = self.table
        table.is_active = True
        table.save()
        super(OrderModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print("delete")
        table = self.table
        table.is_active = False
        table.save()
        print(table.is_active)
        super(OrderModel, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "orders"
