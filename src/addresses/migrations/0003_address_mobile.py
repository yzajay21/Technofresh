# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-03 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20180331_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='mobile',
            field=models.IntegerField(default=9763683339, help_text='Your Mobile Number', max_length=10),
            preserve_default=False,
        ),
    ]
