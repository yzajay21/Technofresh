# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-02 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_billingprofile_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='mobile_no',
            field=models.IntegerField(default=9763683339),
            preserve_default=False,
        ),
    ]
