# Generated by Django 4.2.6 on 2023-11-06 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0009_remove_ordermodel_quantity_ordermodel_weight_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='telegram_id',
            field=models.PositiveBigIntegerField(blank=True, null=True, unique=True, verbose_name='Telegram ID'),
        ),
    ]
