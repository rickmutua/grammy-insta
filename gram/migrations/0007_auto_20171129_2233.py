# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 19:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0006_auto_20171128_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profpic',
            field=models.ImageField(blank=True, default=False, upload_to='profpic/'),
        ),
    ]
