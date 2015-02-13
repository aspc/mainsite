# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('name', models.CharField(max_length=32)),
                ('shortname', models.SlugField(max_length=32)),
                ('type', models.IntegerField(db_index=True, choices=[(0, b'Dormitory'), (1, b'Academic'), (2, b'Dining Hall')])),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField()),
                ('building', models.ForeignKey(to='college.Building')),
            ],
            options={
                'ordering': ('number',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'maps/')),
                ('n', models.FloatField()),
                ('e', models.FloatField()),
                ('s', models.FloatField()),
                ('w', models.FloatField()),
                ('floor', models.OneToOneField(to='college.Floor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoomLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('number', models.CharField(help_text=b'room number in building numbering scheme', max_length=8)),
                ('floor', models.ForeignKey(to='college.Floor')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
            options={
                'ordering': ['-end'],
            },
            bases=(models.Model,),
        ),
    ]
