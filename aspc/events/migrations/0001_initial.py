# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('events', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('eatshop_business')


    models = {
        'eatshop.event': {
            'Meta': {'ordering': "['start', 'name', 'end']", 'object_name': 'Event'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['events']
