# Generated by Django 4.0.5 on 2022-07-04 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_rename_product_amount_product_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='amount',
            new_name='amt',
        ),
    ]