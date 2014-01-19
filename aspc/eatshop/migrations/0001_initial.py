# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Business'
        db.create_table('eatshop_business', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('claremont_cash', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discount', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('www', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('eatshop', ['Business'])

        # Adding model 'Hours'
        db.create_table('eatshop_hours', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hours', to=orm['eatshop.Business'])),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('begin', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('eatshop', ['Hours'])


    def backwards(self, orm):

        # Deleting model 'Business'
        db.delete_table('eatshop_business')

        # Deleting model 'Hours'
        db.delete_table('eatshop_hours')


    models = {
        'eatshop.business': {
            'Meta': {'ordering': "['name']", 'object_name': 'Business'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'claremont_cash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'www': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'eatshop.hours': {
            'Meta': {'ordering': "['begin', 'end']", 'object_name': 'Hours'},
            'begin': ('django.db.models.fields.TimeField', [], {}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hours'", 'to': "orm['eatshop.Business']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['eatshop']
