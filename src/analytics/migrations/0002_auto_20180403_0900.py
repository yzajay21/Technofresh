# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-03 09:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ObjectView',
            new_name='ObjectViewed',
        ),
    ]
