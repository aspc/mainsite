# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Meeting.campus'
        db.add_column('coursesearch_meeting', 'campus', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Meeting.campus'
        db.delete_column('coursesearch_meeting', 'campus')


    models = {
        'coursesearch.course': {
            'Meta': {'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'credit': ('django.db.models.fields.FloatField', [], {}),
            'departments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_set'", 'symmetrical': 'False', 'to': "orm['coursesearch.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grading_style': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'primary_department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_course_set'", 'null': 'True', 'to': "orm['coursesearch.Department']"}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        'coursesearch.department': {
            'Meta': {'object_name': 'Department'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'coursesearch.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'begin': ('django.db.models.fields.TimeField', [], {}),
            'campus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coursesearch.Course']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['coursesearch']
