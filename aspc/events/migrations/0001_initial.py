# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('host', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('status', models.CharField(default=b'pending', max_length=255, choices=[(b'pending', b'Pending'), (b'approved', b'Approved'), (b'denied', b'Denied')])),
            ],
            options={
                'ordering': ('start', 'name', 'end'),
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookEventPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('page_id', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
