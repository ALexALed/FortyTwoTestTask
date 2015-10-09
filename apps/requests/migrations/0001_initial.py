# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestData'
        db.create_table('requests_requestdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('http_request', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('remote_addr', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('requests', ['RequestData'])


    def backwards(self, orm):
        # Deleting model 'RequestData'
        db.delete_table('requests_requestdata')


    models = {
        'requests.requestdata': {
            'Meta': {'object_name': 'RequestData'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'http_request': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_addr': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['requests']