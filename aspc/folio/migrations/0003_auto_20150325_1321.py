# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0002_auto_20150325_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='stylesheet',
            field=models.CharField(help_text=b'Path to an additional stylesheet for this page (relative to /static/css/pages/)', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
