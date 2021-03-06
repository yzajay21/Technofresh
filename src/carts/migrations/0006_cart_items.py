# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_category_image'),
        ('carts', '0005_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='carts.CartItem', to='products.Variation'),
        ),
    ]
