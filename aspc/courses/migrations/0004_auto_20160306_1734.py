# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-06 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_refreshhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='credit',
            field=models.FloatField(default=1.0),
        ),
    ]
