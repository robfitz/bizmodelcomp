# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SiteCopy'
        db.create_table('sitecopy_sitecopy', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('sitecopy', ['SiteCopy'])

        # Adding model 'Testimonial'
        db.create_table('sitecopy_testimonial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('thumb_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('sitecopy', ['Testimonial'])


    def backwards(self, orm):
        
        # Deleting model 'SiteCopy'
        db.delete_table('sitecopy_sitecopy')

        # Deleting model 'Testimonial'
        db.delete_table('sitecopy_testimonial')


    models = {
        'sitecopy.sitecopy': {
            'Meta': {'object_name': 'SiteCopy'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'sitecopy.testimonial': {
            'Meta': {'object_name': 'Testimonial'},
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'author_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'thumb_url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['sitecopy']
