# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b"The page's full title", max_length=255)),
                ('short_title', models.CharField(help_text=b'An optional abbreviated title (for sidebar display)', max_length=80, blank=True)),
                ('slug', models.CharField(help_text=b'The slug (URL identifier) for the page', max_length=80)),
                ('summary', models.TextField(help_text=b"Page summary for display in parent page's subpage list (plain text)", null=True, blank=True)),
                ('body', models.TextField(help_text=b'Page body text written in Markdown', null=True, blank=True)),
                ('sort_order', models.PositiveSmallIntegerField(help_text=b'Sort ordering', blank=True)),
                ('stylesheet', models.CharField(help_text=b'Path to an additional stylesheet for this page (relative to /static/css/pages/)', max_length=255, null=True, blank=True)),
                ('visible', models.BooleanField(default=True, help_text=b'Determines whether a top or second level page will be shown in the sidebar navigation')),
                ('managed', models.BooleanField(default=False, help_text=b"Indicates whether this is a special page that should not be deleted through normal means. (Don't change this unless you know what you're doing!)")),
                ('parent', models.ForeignKey(blank=True, to='folio.Page', help_text=b'Optional parent page for this one. If none, it is treated as a category.', null=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
            bases=(models.Model,),
        ),
    ]
