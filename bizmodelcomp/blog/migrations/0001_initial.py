# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('blog_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('blog', ['Category'])

        # Adding model 'BlogPost'
        db.create_table('blog_blogpost', (
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, primary_key=True)),
            ('custom_title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=10000)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('blog', ['BlogPost'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('blog_category')

        # Deleting model 'BlogPost'
        db.delete_table('blog_blogpost')


    models = {
        'blog.blogpost': {
            'Meta': {'object_name': 'BlogPost'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'custom_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'primary_key': 'True'})
        },
        'blog.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['blog']
