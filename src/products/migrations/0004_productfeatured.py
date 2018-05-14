# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-17 06:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20180315_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeatured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.image_upload_to_featured)),
                ('title', models.CharField(blank=True, max_length=120, null=True)),
                ('text', models.CharField(blank=True, max_length=220, null=True)),
                ('text_right', models.BooleanField(default=False)),
                ('text_css_color', models.CharField(blank=True, max_length=6, null=True)),
                ('show_price', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]
