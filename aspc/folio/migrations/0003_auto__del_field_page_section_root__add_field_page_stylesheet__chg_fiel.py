# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Page.section_root'
        db.delete_column('folio_page', 'section_root')

        # Adding field 'Page.stylesheet'
        db.add_column('folio_page', 'stylesheet', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Changing field 'Page.body'
        db.alter_column('folio_page', 'body', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Page.summary'
        db.alter_column('folio_page', 'summary', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Adding field 'Page.section_root'
        db.add_column('folio_page', 'section_root', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Page.stylesheet'
        db.delete_column('folio_page', 'stylesheet')

        # Changing field 'Page.body'
        db.alter_column('folio_page', 'body', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Page.summary'
        db.alter_column('folio_page', 'summary', self.gf('django.db.models.fields.TextField')(default=''))


    models = {
        'folio.page': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['folio.Page']", 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'stylesheet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['folio']
