# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('posted', models.DateTimeField()),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['posted'],
            },
            bases=(models.Model,),
        ),
    ]
