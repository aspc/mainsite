# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MeetingMinutes'
        db.create_table('minutes_meetingminutes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('minutes', ['MeetingMinutes'])


    def backwards(self, orm):
        
        # Deleting model 'MeetingMinutes'
        db.delete_table('minutes_meetingminutes')


    models = {
        'minutes.meetingminutes': {
            'Meta': {'ordering': "['-date']", 'object_name': 'MeetingMinutes'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['minutes']
