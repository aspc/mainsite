# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Section.course'
        db.add_column(u'courses_section', 'course',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='sections', to=orm['courses.Course']),
                      keep_default=False)

        # Removing M2M table for field course on 'Section'
        db.delete_table(db.shorten_name(u'courses_section_course'))


    def backwards(self, orm):
        # Deleting field 'Section.course'
        db.delete_column(u'courses_section', 'course_id')

        # Adding M2M table for field course on 'Section'
        m2m_table_name = db.shorten_name(u'courses_section_course')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm[u'courses.section'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['section_id', 'course_id'])


    models = {
        u'courses.course': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'code_slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'departments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_set'", 'symmetrical': 'False', 'to': u"orm['courses.Department']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'primary_department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_course_set'", 'null': 'True', 'to': u"orm['courses.Department']"}),
            'requirement_areas': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_set'", 'symmetrical': 'False', 'to': u"orm['courses.RequirementArea']"})
        },
        u'courses.department': {
            'Meta': {'object_name': 'Department'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'courses.instructor': {
            'Meta': {'object_name': 'Instructor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'courses.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'begin': ('django.db.models.fields.TimeField', [], {}),
            'campus': ('django.db.models.fields.SmallIntegerField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'friday': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'monday': ('django.db.models.fields.BooleanField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Section']"}),
            'thursday': ('django.db.models.fields.BooleanField', [], {}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {})
        },
        u'courses.requirementarea': {
            'Meta': {'object_name': 'RequirementArea'},
            'campus': ('django.db.models.fields.SmallIntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'courses.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'create_ts': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Section']", 'symmetrical': 'False'})
        },
        u'courses.section': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Section'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'code_slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['courses.Course']"}),
            'credit': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fee': ('django.db.models.fields.BooleanField', [], {}),
            'filled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grading_style': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sections'", 'symmetrical': 'False', 'to': u"orm['courses.Instructor']"}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'perms': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'requisites': ('django.db.models.fields.BooleanField', [], {}),
            'spots': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['courses.Term']"})
        },
        u'courses.term': {
            'Meta': {'ordering': "['-year', 'session']", 'object_name': 'Term'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['courses']