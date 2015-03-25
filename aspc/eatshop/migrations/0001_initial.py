# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(0, b'On-Campus Restaurant'), (1, b'Restaurant'), (2, b'Snacks & Treats'), (3, b'Beauty and Health'), (4, b'Apparel'), (5, b'Groceries'), (6, b'Other')])),
                ('address', models.TextField()),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True)),
                ('description', models.TextField(help_text=b'Brief description for this business')),
                ('claremont_cash', models.BooleanField()),
                ('flex', models.BooleanField()),
                ('discount', models.TextField(null=True, verbose_name=b'student discount', blank=True)),
                ('www', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'business',
                'verbose_name_plural': 'businesses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monday', models.BooleanField()),
                ('tuesday', models.BooleanField()),
                ('wednesday', models.BooleanField()),
                ('thursday', models.BooleanField()),
                ('friday', models.BooleanField()),
                ('saturday', models.BooleanField()),
                ('sunday', models.BooleanField()),
                ('begin', models.TimeField()),
                ('end', models.TimeField()),
                ('business', models.ForeignKey(related_name='hours', to='eatshop.Business')),
            ],
            options={
                'ordering': ['begin', 'end'],
                'verbose_name': 'hours',
                'verbose_name_plural': 'hours',
            },
            bases=(models.Model,),
        ),
    ]
