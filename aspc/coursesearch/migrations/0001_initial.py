# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Department'
        db.create_table('coursesearch_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('coursesearch', ['Department'])

        # Adding model 'Course'
        db.create_table('coursesearch_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('instructor', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('grading_style', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('credit', self.gf('django.db.models.fields.FloatField')()),
            ('fee', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
            ('primary_department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_course_set', null=True, to=orm['coursesearch.Department'])),
        ))
        db.send_create_signal('coursesearch', ['Course'])

        # Adding M2M table for field departments on 'Course'
        db.create_table('coursesearch_course_departments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['coursesearch.course'], null=False)),
            ('department', models.ForeignKey(orm['coursesearch.department'], null=False))
        ))
        db.create_unique('coursesearch_course_departments', ['course_id', 'department_id'])

        # Adding model 'Meeting'
        db.create_table('coursesearch_meeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coursesearch.Course'])),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('begin', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('coursesearch', ['Meeting'])


    def backwards(self, orm):
        
        # Deleting model 'Department'
        db.delete_table('coursesearch_department')

        # Deleting model 'Course'
        db.delete_table('coursesearch_course')

        # Removing M2M table for field departments on 'Course'
        db.delete_table('coursesearch_course_departments')

        # Deleting model 'Meeting'
        db.delete_table('coursesearch_meeting')


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
