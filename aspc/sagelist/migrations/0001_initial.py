# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('authors', models.CharField(max_length=255, verbose_name=b'Author(s)')),
                ('isbn', models.CharField(max_length=20, null=True, verbose_name=b'ISBN', blank=True)),
                ('edition', models.CharField(max_length=30, null=True, blank=True)),
                ('condition', models.IntegerField(choices=[(0, b'like new'), (1, b'very good'), (2, b'good'), (3, b'usable')])),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('is_recoop', models.BooleanField(default=False)),
                ('recoop_id', models.IntegerField(unique=True, null=True)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(related_name='book_purchases_set', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('seller', models.ForeignKey(related_name='book_sales_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['posted'],
            },
            bases=(models.Model,),
        ),
    ]
