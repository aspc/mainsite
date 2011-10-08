# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Floor'
        db.create_table('college_floor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Building'])),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('college', ['Floor'])

        # Adding model 'Building'
        db.create_table('college_building', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('shortname', self.gf('django.db.models.fields.SlugField')(max_length=32, db_index=True)),
        ))
        db.send_create_signal('college', ['Building'])

        # Adding model 'RoomLocation'
        db.create_table('college_roomlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Floor'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('college', ['RoomLocation'])


    def backwards(self, orm):
        
        # Deleting model 'Floor'
        db.delete_table('college_floor')

        # Deleting model 'Building'
        db.delete_table('college_building')

        # Deleting model 'RoomLocation'
        db.delete_table('college_roomlocation')


    models = {
        'college.building': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Building'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'college.floor': {
            'Meta': {'ordering': "('number',)", 'object_name': 'Floor'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['college.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'college.roomlocation': {
            'Meta': {'object_name': 'RoomLocation'},
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['college.Floor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'college.term': {
            'Meta': {'ordering': "['-end']", 'object_name': 'Term'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['college']
