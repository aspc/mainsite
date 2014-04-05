# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Term'
        db.create_table(u'courses_term', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('subsession', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal(u'courses', ['Term'])

        # Adding model 'Instructor'
        db.create_table(u'courses_instructor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'courses', ['Instructor'])

        # Adding model 'Department'
        db.create_table(u'courses_department', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'courses', ['Department'])

        # Adding model 'RequirementArea'
        db.create_table(u'courses_requirementarea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('campus', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'courses', ['RequirementArea'])

        # Adding model 'Course'
        db.create_table(u'courses_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('code_slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('primary_department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_course_set', null=True, to=orm['courses.Department'])),
        ))
        db.send_create_signal(u'courses', ['Course'])

        # Adding M2M table for field departments on 'Course'
        m2m_table_name = db.shorten_name(u'courses_course_departments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False)),
            ('department', models.ForeignKey(orm[u'courses.department'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'department_id'])

        # Adding M2M table for field requirement_areas on 'Course'
        m2m_table_name = db.shorten_name(u'courses_course_requirement_areas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False)),
            ('requirementarea', models.ForeignKey(orm[u'courses.requirementarea'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'requirementarea_id'])

        # Adding model 'Section'
        db.create_table(u'courses_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['courses.Term'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('code_slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('grading_style', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('credit', self.gf('django.db.models.fields.FloatField')()),
            ('requisites', self.gf('django.db.models.fields.BooleanField')()),
            ('fee', self.gf('django.db.models.fields.BooleanField')()),
            ('perms', self.gf('django.db.models.fields.IntegerField')()),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
            ('filled', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'courses', ['Section'])

        # Adding M2M table for field course on 'Section'
        m2m_table_name = db.shorten_name(u'courses_section_course')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm[u'courses.section'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['section_id', 'course_id'])

        # Adding M2M table for field instructors on 'Section'
        m2m_table_name = db.shorten_name(u'courses_section_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm[u'courses.section'], null=False)),
            ('instructor', models.ForeignKey(orm[u'courses.instructor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['section_id', 'instructor_id'])

        # Adding model 'Meeting'
        db.create_table(u'courses_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Section'])),
            ('monday', self.gf('django.db.models.fields.BooleanField')()),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')()),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')()),
            ('thursday', self.gf('django.db.models.fields.BooleanField')()),
            ('friday', self.gf('django.db.models.fields.BooleanField')()),
            ('begin', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('campus', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'courses', ['Meeting'])

        # Adding model 'Schedule'
        db.create_table(u'courses_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_ts', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'courses', ['Schedule'])

        # Adding M2M table for field sections on 'Schedule'
        m2m_table_name = db.shorten_name(u'courses_schedule_sections')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm[u'courses.schedule'], null=False)),
            ('section', models.ForeignKey(orm[u'courses.section'], null=False))
        ))
        db.create_unique(m2m_table_name, ['schedule_id', 'section_id'])


    def backwards(self, orm):
        # Deleting model 'Term'
        db.delete_table(u'courses_term')

        # Deleting model 'Instructor'
        db.delete_table(u'courses_instructor')

        # Deleting model 'Department'
        db.delete_table(u'courses_department')

        # Deleting model 'RequirementArea'
        db.delete_table(u'courses_requirementarea')

        # Deleting model 'Course'
        db.delete_table(u'courses_course')

        # Removing M2M table for field departments on 'Course'
        db.delete_table(db.shorten_name(u'courses_course_departments'))

        # Removing M2M table for field requirement_areas on 'Course'
        db.delete_table(db.shorten_name(u'courses_course_requirement_areas'))

        # Deleting model 'Section'
        db.delete_table(u'courses_section')

        # Removing M2M table for field course on 'Section'
        db.delete_table(db.shorten_name(u'courses_section_course'))

        # Removing M2M table for field instructors on 'Section'
        db.delete_table(db.shorten_name(u'courses_section_instructors'))

        # Deleting model 'Meeting'
        db.delete_table(u'courses_meeting')

        # Deleting model 'Schedule'
        db.delete_table(u'courses_schedule')

        # Removing M2M table for field sections on 'Schedule'
        db.delete_table(db.shorten_name(u'courses_schedule_sections'))


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
            'course': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sections'", 'symmetrical': 'False', 'to': u"orm['courses.Course']"}),
            'credit': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fee': ('django.db.models.fields.BooleanField', [], {}),
            'filled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grading_style': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sections'", 'symmetrical': 'False', 'to': u"orm['courses.Instructor']"}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'perms': ('django.db.models.fields.IntegerField', [], {}),
            'requisites': ('django.db.models.fields.BooleanField', [], {}),
            'spots': ('django.db.models.fields.IntegerField', [], {}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['courses.Term']"})
        },
        u'courses.term': {
            'Meta': {'ordering': "['-year', 'session', '-subsession']", 'object_name': 'Term'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'subsession': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['courses']