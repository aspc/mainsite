# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=20, db_index=True)),
                ('code_slug', models.CharField(unique=True, max_length=20, db_index=True)),
                ('number', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('code',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=20, db_index=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monday', models.BooleanField()),
                ('tuesday', models.BooleanField()),
                ('wednesday', models.BooleanField()),
                ('thursday', models.BooleanField()),
                ('friday', models.BooleanField()),
                ('begin', models.TimeField()),
                ('end', models.TimeField()),
                ('campus', models.SmallIntegerField(choices=[(1, 'PO'), (2, 'SC'), (3, 'CMC'), (4, 'HM'), (5, 'PZ'), (6, 'CGU'), (7, 'CU'), (8, 'KS'), (-1, '?')])),
                ('location', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequirementArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=20, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('campus', models.SmallIntegerField(choices=[(1, 'PO'), (2, 'SC'), (3, 'CMC'), (4, 'HM'), (5, 'PZ'), (6, 'CGU'), (7, 'CU'), (8, 'KS'), (-1, '?')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_ts', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('code_slug', models.CharField(max_length=20)),
                ('grading_style', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('credit', models.FloatField()),
                ('requisites', models.BooleanField()),
                ('fee', models.BooleanField()),
                ('perms', models.IntegerField(null=True)),
                ('spots', models.IntegerField(null=True)),
                ('filled', models.IntegerField(null=True, blank=True)),
                ('course', models.ForeignKey(related_name='sections', to='courses.Course')),
                ('instructors', models.ManyToManyField(related_name='sections', to='courses.Instructor')),
            ],
            options={
                'ordering': ('code',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=20)),
                ('year', models.PositiveSmallIntegerField()),
                ('session', models.CharField(max_length=2, choices=[('SP', 'Spring'), ('FA', 'Fall')])),
            ],
            options={
                'ordering': ['-year', 'session'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='section',
            name='term',
            field=models.ForeignKey(related_name='sections', to='courses.Term'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedule',
            name='sections',
            field=models.ManyToManyField(to='courses.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='section',
            field=models.ForeignKey(to='courses.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='departments',
            field=models.ManyToManyField(related_name='course_set', to='courses.Department'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='primary_department',
            field=models.ForeignKey(related_name='primary_course_set', to='courses.Department', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='requirement_areas',
            field=models.ManyToManyField(related_name='course_set', to='courses.RequirementArea'),
            preserve_default=True,
        ),
    ]
