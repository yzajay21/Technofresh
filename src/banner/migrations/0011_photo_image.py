# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-20 15:27
from __future__ import unicode_literals

import banner.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0010_auto_20180420_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image',
            field=models.ImageField(default=datetime.datetime(2018, 4, 20, 15, 27, 36, 223572, tzinfo=utc), upload_to=banner.models.image_upload_to),
            preserve_default=False,
        ),
    ]
