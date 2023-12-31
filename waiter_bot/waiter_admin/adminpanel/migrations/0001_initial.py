# Generated by Django 4.2.6 on 2023-10-19 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='CompanyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone number')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last name')),
                ('user_type', models.CharField(choices=[('super_admin', 'SuperAdmin'), ('admin', 'Admin'), ('waiter', 'Waiter'), ('cashier', 'Cashier')], default='waiter', max_length=255, verbose_name='User type')),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Username')),
                ('password', models.CharField(max_length=255, verbose_name='Password')),
                ('telegram_id', models.PositiveBigIntegerField(unique=True, verbose_name='Telegram ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/', verbose_name='Photo')),
                ('auth_status', models.BooleanField(default=False, verbose_name='Auth status')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='adminpanel.companymodel', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='TableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='adminpanel.companymodel', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Table',
                'verbose_name_plural': 'Tables',
                'db_table': 'tables',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('price', models.PositiveBigIntegerField(verbose_name='Price')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Photo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='adminpanel.categorymodel', verbose_name='Category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='adminpanel.companymodel', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('status', models.CharField(choices=[('new', 'New'), ('in_process', 'In process'), ('done', 'Done')], default='new', max_length=255, verbose_name='Status')),
                ('quantity', models.PositiveBigIntegerField(verbose_name='Quantity')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='adminpanel.companymodel', verbose_name='Company')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='adminpanel.productmodel', verbose_name='Product')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='adminpanel.tablemodel', verbose_name='Table')),
                ('waiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='adminpanel.usermodel', verbose_name='Waiter')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'orders',
            },
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='adminpanel.companymodel', verbose_name='Company'),
        ),
    ]
