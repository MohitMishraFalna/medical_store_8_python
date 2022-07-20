# Generated by Django 4.0.5 on 2022-07-05 09:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_quantity_product_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='expiry',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturing',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]
