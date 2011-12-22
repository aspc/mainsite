# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Page.visible'
        db.add_column('folio_page', 'visible', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'Page.managed'
        db.add_column('folio_page', 'managed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Page.visible'
        db.delete_column('folio_page', 'visible')

        # Deleting field 'Page.managed'
        db.delete_column('folio_page', 'managed')


    models = {
        'folio.page': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['folio.Page']", 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'stylesheet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['folio']
