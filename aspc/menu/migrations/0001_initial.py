# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Menu'
        db.create_table(u'menu_menu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dining_hall', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meal', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'menu', ['Menu'])


    def backwards(self, orm):
        # Deleting model 'Menu'
        db.delete_table(u'menu_menu')


    models = {
        u'menu.menu': {
            'Meta': {'ordering': "('day', 'dining_hall', 'meal')", 'object_name': 'Menu'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dining_hall': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['menu']