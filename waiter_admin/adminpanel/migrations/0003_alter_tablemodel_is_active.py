# Generated by Django 4.2.6 on 2023-10-19 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0002_tablemodel_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablemodel',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is active'),
        ),
    ]
