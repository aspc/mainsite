# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SocialMediaActivity'
        db.delete_table('activityfeed_socialmediaactivity')

        # Adding model 'TwitterActivity'
        db.create_table('activityfeed_twitteractivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tweet_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('activityfeed', ['TwitterActivity'])


        # Changing field 'Activity.date'
        db.alter_column('activityfeed_activity', 'date', self.gf('django.db.models.fields.DateTimeField')())
    def backwards(self, orm):
        # Adding model 'SocialMediaActivity'
        db.create_table('activityfeed_socialmediaactivity', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('activityfeed', ['SocialMediaActivity'])

        # Deleting model 'TwitterActivity'
        db.delete_table('activityfeed_twitteractivity')


        # Changing field 'Activity.date'
        db.alter_column('activityfeed_activity', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
    models = {
        'activityfeed.activity': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Activity'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'activityfeed.twitteractivity': {
            'Meta': {'ordering': "['-tweet_id']", 'object_name': 'TwitterActivity'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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