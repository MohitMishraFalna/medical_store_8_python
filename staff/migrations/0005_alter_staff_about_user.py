# Generated by Django 4.0.5 on 2022-06-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_staff_about_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='about_user',
            field=models.CharField(default='', max_length=250),
        ),
    ]
