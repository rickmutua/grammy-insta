# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 10:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gram', '0011_remove_post_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.PositiveIntegerField(blank=True, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gram.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]