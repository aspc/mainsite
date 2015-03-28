# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='login_id',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Login ID', blank=True),
            preserve_default=True,
        ),
    ]
