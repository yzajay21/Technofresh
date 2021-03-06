# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-17 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productfeatured'),
        ('carts', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('line_item_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Variation')),
            ],
        ),
    ]
