# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingMinutes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(help_text=b'Date of the meeting')),
                ('summary', models.TextField(help_text=b'Summarize this meeting in a sentence or two of unformatted text. (Used for search results and overview.)', blank=True)),
                ('body', models.TextField(help_text=b'The minutes of this meeting in <a href="http://daringfireball.net/projects/markdown/dingus">Markdown</a>', blank=True)),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'meeting minutes',
                'verbose_name_plural': 'meeting minutes',
            },
            bases=(models.Model,),
        ),
    ]
