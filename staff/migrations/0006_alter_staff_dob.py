# Generated by Django 4.0.5 on 2022-06-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_alter_staff_about_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='dob',
            field=models.DateField(default=''),
        ),
    ]