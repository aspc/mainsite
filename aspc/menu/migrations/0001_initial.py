# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dining_hall', models.CharField(max_length=255, choices=[(b'frank', b'Frank'), (b'frary', b'Frary'), (b'oldenborg', b'Oldenborg'), (b'scripps', b'Scripps'), (b'mudd', b'Mudd'), (b'cmc', b'CMC'), (b'pitzer', b'Pitzer')])),
                ('meal', models.CharField(max_length=255, choices=[(b'breakfast', b'Breakfast'), (b'lunch', b'Lunch'), (b'dinner', b'Dinner'), (b'brunch', b'Brunch')])),
                ('day', models.CharField(max_length=255, choices=[(b'mon', b'Monday'), (b'tue', b'Tuesday'), (b'wed', b'Wednesday'), (b'thu', b'Thursday'), (b'fri', b'Friday'), (b'sat', b'Saturday'), (b'sun', b'Sunday')])),
                ('food_items', models.TextField()),
            ],
            options={
                'ordering': ('day', 'dining_hall', 'meal'),
                'verbose_name_plural': 'Menus',
            },
            bases=(models.Model,),
        ),
    ]
