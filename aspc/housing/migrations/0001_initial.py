# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_ts', models.DateTimeField(auto_now_add=True, verbose_name=b'posted at')),
                ('overall', models.FloatField(editable=False)),
                ('quiet', models.IntegerField(default=2, choices=[(0, 'noisy'), (1, 'some noise'), (2, 'average'), (3, 'quieter than average'), (4, 'quiet')])),
                ('spacious', models.IntegerField(default=2, choices=[(0, 'cramped'), (1, 'small'), (2, 'adequate'), (3, 'roomy'), (4, 'spacious')])),
                ('temperate', models.IntegerField(default=2, choices=[(0, 'too hot/cold'), (1, 'slightly uncomfortable'), (2, 'tolerable'), (3, 'comfortable'), (4, 'perfect')])),
                ('maintained', models.IntegerField(default=2, choices=[(0, 'run-down'), (1, 'tatty'), (2, 'average'), (3, 'presentable'), (4, 'well maintained')])),
                ('cellphone', models.IntegerField(default=2, choices=[(0, 'no cell service'), (1, 'some cell service'), (2, 'average  cell service'), (3, 'good cell service'), (4, 'excellent cell service')])),
                ('best', models.TextField()),
                ('worst', models.TextField()),
                ('comments', models.TextField(blank=True)),
                ('photo1', stdimage.fields.StdImageField(null=True, upload_to=b'housing/reviews/%Y/%m/%d/', blank=True)),
                ('photo2', stdimage.fields.StdImageField(null=True, upload_to=b'housing/reviews/%Y/%m/%d/', blank=True)),
                ('photo3', stdimage.fields.StdImageField(null=True, upload_to=b'housing/reviews/%Y/%m/%d/', blank=True)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-create_ts'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('roomlocation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='college.RoomLocation')),
                ('size', models.FloatField(help_text=b'size in square feet', null=True, blank=True)),
                ('occupancy', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'single'), (2, b'double'), (3, b'two room double'), (4, b'two room triple')])),
                ('reserved', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(0, b'freshman housing'), (1, b'RHS')])),
                ('average_rating', models.FloatField(null=True, editable=False, blank=True)),
                ('average_rating_quiet', models.FloatField(null=True, editable=False, blank=True)),
                ('average_rating_spacious', models.FloatField(null=True, editable=False, blank=True)),
                ('average_rating_temperate', models.FloatField(null=True, editable=False, blank=True)),
                ('average_rating_maintained', models.FloatField(null=True, editable=False, blank=True)),
                ('average_rating_cellphone', models.FloatField(null=True, editable=False, blank=True)),
            ],
            options={
                'ordering': ('number',),
            },
            bases=('college.roomlocation',),
        ),
        migrations.CreateModel(
            name='Suite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occupancy', models.IntegerField(choices=[(3, b'three person'), (4, b'four person'), (5, b'five person'), (6, b'six person')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='room',
            name='suite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='housing.Suite', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='review',
            name='room',
            field=models.ForeignKey(to='housing.Room'),
            preserve_default=True,
        ),
    ]
