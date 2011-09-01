# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('folio_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['folio.Page'], null=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('section', self.gf('django.db.models.fields.IntegerField')()),
            ('sort_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
        ))
        db.send_create_signal('folio', ['Page'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('folio_page')


    models = {
        'folio.page': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['folio.Page']", 'null': 'True'}),
            'section': ('django.db.models.fields.IntegerField', [], {}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['folio']
