# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Bulk_email.recipient_founders'
        db.add_column('emailhelper_bulk_email', 'recipient_founders', self.gf('django.db.models.fields.CharField')(default='', max_length=10000), keep_default=False)

        # Removing M2M table for field recipient_founders on 'Bulk_email'
        db.delete_table('emailhelper_bulk_email_recipient_founders')


    def backwards(self, orm):
        
        # Deleting field 'Bulk_email.recipient_founders'
        db.delete_column('emailhelper_bulk_email', 'recipient_founders')

        # Adding M2M table for field recipient_founders on 'Bulk_email'
        db.create_table('emailhelper_bulk_email_recipient_founders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bulk_email', models.ForeignKey(orm['emailhelper.bulk_email'], null=False)),
            ('founder', models.ForeignKey(orm['competition.founder'], null=False))
        ))
        db.create_unique('emailhelper_bulk_email_recipient_founders', ['bulk_email_id', 'founder_id'])


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
            'Meta': {'object_name': 'Val'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_val': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emailhelper.Sub_val']"}),
            'val': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['emailhelper']
