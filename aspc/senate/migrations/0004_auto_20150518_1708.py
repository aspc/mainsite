# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senate', '0003_auto_20150328_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
