# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialMediaActivity'
        db.create_table('activityfeed_socialmediaactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('activityfeed', ['SocialMediaActivity'])

        # Deleting field 'Activity.url'
        db.delete_column('activityfeed_activity', 'url')

        # Deleting field 'Activity.message'
        db.delete_column('activityfeed_activity', 'message')

    def backwards(self, orm):
        # Deleting model 'SocialMediaActivity'
        db.delete_table('activityfeed_socialmediaactivity')

        # Adding field 'Activity.url'
        db.add_column('activityfeed_activity', 'url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Activity.message'
        db.add_column('activityfeed_activity', 'message',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

    models = {
        'activityfeed.activity': {
            'Meta': {'object_name': 'Activity'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'activityfeed.socialmediaactivity': {
            'Meta': {'object_name': 'SocialMediaActivity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['activityfeed']