# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('category', models.CharField(max_length=100, choices=[(b'housing', b'Housing Reviews'), (b'sagelist', b'SageBooks'), (b'twitter', b'Twitter')])),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('url', models.URLField()),
                ('message', models.TextField()),
                ('author', models.CharField(max_length=20)),
                ('tweet_id', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-tweet_id'],
            },
            bases=(models.Model,),
        ),
    ]
