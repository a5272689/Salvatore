# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-21 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('silas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='seat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assets_set', to='silas.Seat'),
            preserve_default=False,
        ),
    ]
