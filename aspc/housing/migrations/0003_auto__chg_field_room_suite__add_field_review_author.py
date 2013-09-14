# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Room.suite'
        db.alter_column('housing_room', 'suite_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['housing.Suite'], null=True, on_delete=models.SET_NULL))
        # Adding field 'Review.author'
        db.add_column('housing_review', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):

        # Changing field 'Room.suite'
        db.alter_column('housing_room', 'suite_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['housing.Suite'], null=True))
        # Deleting field 'Review.author'
        db.delete_column('housing_review', 'author_id')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'college.building': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Building'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'housing.review': {
            'Meta': {'ordering': "['-create_ts']", 'object_name': 'Review'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
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
            'suite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['housing.Suite']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'housing.suite': {
            'Meta': {'object_name': 'Suite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occupancy': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['housing']