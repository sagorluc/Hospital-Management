# Generated by Django 5.0.2 on 2024-03-21 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='additional_address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(null=True),
        ),
    ]
