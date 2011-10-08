# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Room'
        db.create_table('housing_room', (
            ('roomlocation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['college.RoomLocation'], unique=True, primary_key=True)),
            ('size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('occupancy', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('reserved', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('suite', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('average_rating', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('average_rating_quiet', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('average_rating_spacious', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('average_rating_temperate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('average_rating_maintained', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('average_rating_cellphone', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('housing', ['Room'])

        # Adding model 'Review'
        db.create_table('housing_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_ts', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['housing.Room'])),
            ('overall', self.gf('django.db.models.fields.FloatField')()),
            ('quiet', self.gf('django.db.models.fields.IntegerField')()),
            ('spacious', self.gf('django.db.models.fields.IntegerField')()),
            ('temperate', self.gf('django.db.models.fields.IntegerField')()),
            ('maintained', self.gf('django.db.models.fields.IntegerField')()),
            ('cellphone', self.gf('django.db.models.fields.IntegerField')()),
            ('best', self.gf('django.db.models.fields.TextField')()),
            ('worst', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('housing', ['Review'])


    def backwards(self, orm):
        
        # Deleting model 'Room'
        db.delete_table('housing_room')

        # Deleting model 'Review'
        db.delete_table('housing_review')


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
        'housing.review': {
            'Meta': {'ordering': "['-create_ts']", 'object_name': 'Review'},
            'best': ('django.db.models.fields.TextField', [], {}),
            'cellphone': ('django.db.models.fields.IntegerField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'create_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintained': ('django.db.models.fields.IntegerField', [], {}),
            'overall': ('django.db.models.fields.FloatField', [], {}),
            'quiet': ('django.db.models.fields.IntegerField', [], {}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['housing.Room']"}),
            'spacious': ('django.db.models.fields.IntegerField', [], {}),
            'temperate': ('django.db.models.fields.IntegerField', [], {}),
            'worst': ('django.db.models.fields.TextField', [], {})
        },
        'housing.room': {
            'Meta': {'ordering': "('number',)", 'object_name': 'Room', '_ormbases': ['college.RoomLocation']},
            'average_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'average_rating_cellphone': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'average_rating_maintained': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'average_rating_quiet': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'average_rating_spacious': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'average_rating_temperate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'occupancy': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reserved': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'roomlocation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['college.RoomLocation']", 'unique': 'True', 'primary_key': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'suite': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['housing']
