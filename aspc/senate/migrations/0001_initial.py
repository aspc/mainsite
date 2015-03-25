# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name to display on the Senate Positions page', max_length=40)),
                ('login_id', models.CharField(max_length=20, null=True, verbose_name=b'Login ID', blank=True)),
                ('start', models.DateField()),
                ('end', models.DateField(null=True, blank=True)),
                ('bio', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-end', 'position__sort_order', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('authors', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to=b'senate/documents/%Y/%m/%d/')),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['uploaded_at', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The official title of the position', max_length=80)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('description', models.TextField(help_text=b'(optional) Description of the position', blank=True)),
                ('active', models.BooleanField(default=True, help_text=b'Whether or not a position is still active (for display in the list of Senate positions)')),
                ('sort_order', models.PositiveSmallIntegerField(help_text=b'Sort ordering', blank=True)),
                ('appointments', models.ManyToManyField(help_text=b'Current and past appointees to this position', to=settings.AUTH_USER_MODEL, through='senate.Appointment')),
                ('groups', models.ManyToManyField(help_text=b'Groups that people holding this position should be added to assign the correct permissions.', to='auth.Group', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='appointment',
            name='position',
            field=models.ForeignKey(to='senate.Position'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
