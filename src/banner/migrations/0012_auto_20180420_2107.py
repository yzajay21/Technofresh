# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-20 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0011_photo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='height',
            field=models.IntegerField(default=450),
        ),
        migrations.AddField(
            model_name='photo',
            name='width',
            field=models.IntegerField(default=1380),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank='False', height_field='height', null='False', upload_to='mediafiles', width_field='width'),
        ),
    ]
