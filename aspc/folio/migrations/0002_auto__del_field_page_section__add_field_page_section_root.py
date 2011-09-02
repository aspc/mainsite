# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Page.section'
        db.delete_column('folio_page', 'section')

        # Adding field 'Page.section_root'
        db.add_column('folio_page', 'section_root', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Page.section'
        db.add_column('folio_page', 'section', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Page.section_root'
        db.delete_column('folio_page', 'section_root')


    models = {
        'folio.page': {
            'Meta': {'ordering': "['parent', 'sort_order']", 'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['folio.Page']", 'null': 'True', 'blank': 'True'}),
            'section_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['folio']
