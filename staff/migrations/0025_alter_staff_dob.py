# Generated by Django 4.0.5 on 2022-06-23 05:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0024_alter_staff_login_attempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='dob',
            field=models.DateField(default=datetime.datetime(2022, 6, 23, 5, 44, 28, 266539, tzinfo=utc)),
        ),
    ]