# Generated by Django 5.0.2 on 2024-03-24 11:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_alter_profile_profile_pic_deactivateaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deactivateaccount',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deactivate_user', to=settings.AUTH_USER_MODEL),
        ),
    ]