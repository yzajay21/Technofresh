# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(blank=True, to='products.Category')),
                ('default', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_category', to='products.Category')),
            ],
            options={
                'ordering': ['-title'],
            },
        ),
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
                ('make_image_background', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.image_upload_to)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]
