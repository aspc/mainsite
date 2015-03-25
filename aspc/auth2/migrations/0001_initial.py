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
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=255, null=True, blank=True)),
                ('college', models.CharField(default=b'POM', max_length=255, choices=[(b'POM', b'Pomona'), (b'CMC', b'Claremont McKenna'), (b'SC', b'Scripps'), (b'PZ', b'Pitzer'), (b'HMC', b'Harvey Mudd')])),
                ('year', models.IntegerField(null=True, blank=True)),
                ('dorm', models.CharField(max_length=255, null=True, blank=True)),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'user data',
            },
            bases=(models.Model,),
        ),
    ]
