# Generated by Django 4.0.5 on 2022-06-24 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0028_alter_staff_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='deleted_at',
            field=models.BooleanField(default=0),
        ),
    ]
