# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 15:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offersimages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='height',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='width',
        ),
    ]
