# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Map'
        db.create_table('college_map', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('n', self.gf('django.db.models.fields.FloatField')()),
            ('e', self.gf('django.db.models.fields.FloatField')()),
            ('s', self.gf('django.db.models.fields.FloatField')()),
            ('w', self.gf('django.db.models.fields.FloatField')()),
            ('floor', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['college.Floor'], unique=True)),
        ))
        db.send_create_signal('college', ['Map'])

        # Adding index on 'Building', fields ['type']
        db.create_index('college_building', ['type'])


    def backwards(self, orm):
        
        # Removing index on 'Building', fields ['type']
        db.delete_index('college_building', ['type'])

        # Deleting model 'Map'
        db.delete_table('college_map')


    models = {
        'college.building': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Building'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'college.floor': {
            'Meta': {'ordering': "('number',)", 'object_name': 'Floor'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['college.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'college.map': {
            'Meta': {'object_name': 'Map'},
            'e': ('django.db.models.fields.FloatField', [], {}),
            'floor': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['college.Floor']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'n': ('django.db.models.fields.FloatField', [], {}),
            's': ('django.db.models.fields.FloatField', [], {}),
            'w': ('django.db.models.fields.FloatField', [], {})
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
