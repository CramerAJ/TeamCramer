# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-03 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewards_app', '0012_auto_20170430_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]