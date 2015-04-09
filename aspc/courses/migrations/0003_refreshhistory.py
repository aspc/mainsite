# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20150212_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('run_date', models.DateTimeField(default=datetime.datetime.now)),
                ('last_refresh_date', models.DateTimeField()),
                ('type', models.IntegerField(choices=[(0, b'Full'), (1, b'Registration')])),
                ('term', models.ForeignKey(related_name='term', to='courses.Term')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
