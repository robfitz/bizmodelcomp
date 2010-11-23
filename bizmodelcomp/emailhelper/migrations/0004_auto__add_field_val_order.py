# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Val.order'
        db.add_column('emailhelper_val', 'order', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Val.order'
        db.delete_column('emailhelper_val', 'order')


    models = {
        'emailhelper.bulk_email': {
            'Meta': {'object_name': 'Bulk_email'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_markdown': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'recipient_founders': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'sent_on_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'emailhelper.sub_val': {
            'Meta': {'object_name': 'Sub_val'},
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emailhelper.Bulk_email']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'emailhelper.val': {
            'Meta': {'ordering': "['order']", 'object_name': 'Val'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'sub_val': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emailhelper.Sub_val']"}),
            'val': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['emailhelper']
