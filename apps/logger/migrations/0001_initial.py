# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MyBio'
        db.create_table(u'logger_mybio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('biography', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contacts', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'logger', ['MyBio'])

        # Adding model 'HttpRequestSave'
        db.create_table(u'logger_httprequestsave', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('http_request', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('remote_addr', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
            ('datatime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'logger', ['HttpRequestSave'])

        # Adding model 'DbSignals'
        db.create_table(u'logger_dbsignals', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signal', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'logger', ['DbSignals'])


    def backwards(self, orm):
        # Deleting model 'MyBio'
        db.delete_table(u'logger_mybio')

        # Deleting model 'HttpRequestSave'
        db.delete_table(u'logger_httprequestsave')

        # Deleting model 'DbSignals'
        db.delete_table(u'logger_dbsignals')


    models = {
        u'logger.dbsignals': {
            'Meta': {'object_name': 'DbSignals'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'signal': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'logger.httprequestsave': {
            'Meta': {'object_name': 'HttpRequestSave'},
            'datatime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'http_request': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'remote_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'logger.mybio': {
            'Meta': {'object_name': 'MyBio'},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'contacts': ('django.db.models.fields.TextField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['logger']