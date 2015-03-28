# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senate', '0002_auto_20150328_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='login_id',
            field=models.CharField(help_text=b"The user's email address.", max_length=50, null=True, verbose_name=b'Login ID', blank=True),
            preserve_default=True,
        ),
    ]
