# Generated by Django 4.0.5 on 2022-06-21 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0018_alter_staff_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='profile_img',
            field=models.ImageField(default='profile-img.jpg', upload_to='profileImage/'),
        ),
    ]