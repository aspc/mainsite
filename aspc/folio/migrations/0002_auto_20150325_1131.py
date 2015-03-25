# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='stylesheet',
            field=models.CharField(help_text=b'Path to an additional stylesheet for this page (relative to https://staging.aspc.pomona.edu/static/css/pages/)', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]