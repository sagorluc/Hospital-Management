# Generated by Django 5.0.2 on 2024-03-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_customuser_password_alter_customuser_show_pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(max_length=100),
        ),
    ]