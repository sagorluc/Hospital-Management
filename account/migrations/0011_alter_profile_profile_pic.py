# Generated by Django 5.0.2 on 2024-03-21 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='photos/doctor-icon.jpg', null=True, upload_to='photos/'),
        ),
    ]
