# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RequirementArea'
        db.create_table('coursesearch_requirementarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('campus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('coursesearch', ['RequirementArea'])

        # Adding M2M table for field requirement_areas on 'Course'
        db.create_table('coursesearch_course_requirement_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['coursesearch.course'], null=False)),
            ('requirementarea', models.ForeignKey(orm['coursesearch.requirementarea'], null=False))
        ))
        db.create_unique('coursesearch_course_requirement_areas', ['course_id', 'requirementarea_id'])


    def backwards(self, orm):
        
        # Deleting model 'RequirementArea'
        db.delete_table('coursesearch_requirementarea')

        # Removing M2M table for field requirement_areas on 'Course'
        db.delete_table('coursesearch_course_requirement_areas')


    models = {
        'coursesearch.course': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'code_slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'credit': ('django.db.models.fields.FloatField', [], {}),
            'departments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_set'", 'symmetrical': 'False', 'to': "orm['coursesearch.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grading_style': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'primary_department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_course_set'", 'null': 'True', 'to': "orm['coursesearch.Department']"}),
            'requirement_areas': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_set'", 'symmetrical': 'False', 'to': "orm['coursesearch.RequirementArea']"}),
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
        },
        'coursesearch.requirementarea': {
            'Meta': {'object_name': 'RequirementArea'},
            'campus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'coursesearch.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coursesearch.Course']", 'symmetrical': 'False'}),
            'create_ts': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['coursesearch']
