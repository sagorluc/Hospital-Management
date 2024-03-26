# Generated by Django 5.0.2 on 2024-03-21 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_additional_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work_place',
            field=models.CharField(max_length=100, null=True),
        ),
    ]