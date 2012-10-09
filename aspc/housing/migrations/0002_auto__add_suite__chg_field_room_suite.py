# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Suite'
        db.create_table('housing_suite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('occupancy', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('housing', ['Suite'])

        # Renaming column for 'Room.suite' to match new field type.
        db.rename_column('housing_room', 'suite', 'suite_id')
        # Changing field 'Room.suite'
        db.alter_column('housing_room', 'suite_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['housing.Suite'], null=True))
        
        if not db.backend_name == 'sqlite3':
            # Adding index on 'Room', fields ['suite']
            db.create_index('housing_room', ['suite_id'])


    def backwards(self, orm):
        if not db.backend_name == 'sqlite3':
            # Removing index on 'Room', fields ['suite']
            db.delete_index('housing_room', ['suite_id'])

        # Deleting model 'Suite'
        db.delete_table('housing_suite')

        # Renaming column for 'Room.suite' to match new field type.
        db.rename_column('housing_room', 'suite_id', 'suite')
        # Changing field 'Room.suite'
        db.alter_column('housing_room', 'suite', self.gf('django.db.models.fields.IntegerField')(null=True))


    models = {
        'college.building': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Building'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
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
            'cellphone': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'create_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintained': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'overall': ('django.db.models.fields.FloatField', [], {}),
            'quiet': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['housing.Room']"}),
            'spacious': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'temperate': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
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
            'suite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['housing.Suite']", 'null': 'True'})
        },
        'housing.suite': {
            'Meta': {'object_name': 'Suite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occupancy': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['housing']
