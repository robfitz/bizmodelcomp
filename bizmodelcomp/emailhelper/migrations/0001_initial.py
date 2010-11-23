# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Bulk_email'
        db.create_table('emailhelper_bulk_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('message_markdown', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('sent_on_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('emailhelper', ['Bulk_email'])

        # Adding M2M table for field recipients on 'Bulk_email'
        db.create_table('emailhelper_bulk_email_recipients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bulk_email', models.ForeignKey(orm['emailhelper.bulk_email'], null=False)),
            ('founder', models.ForeignKey(orm['competition.founder'], null=False))
        ))
        db.create_unique('emailhelper_bulk_email_recipients', ['bulk_email_id', 'founder_id'])

        # Adding model 'Sub_val'
        db.create_table('emailhelper_sub_val', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emailhelper.Bulk_email'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('emailhelper', ['Sub_val'])

        # Adding model 'Val'
        db.create_table('emailhelper_val', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sub_val', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emailhelper.Sub_val'])),
            ('val', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('emailhelper', ['Val'])


    def backwards(self, orm):
        
        # Deleting model 'Bulk_email'
        db.delete_table('emailhelper_bulk_email')

        # Removing M2M table for field recipients on 'Bulk_email'
        db.delete_table('emailhelper_bulk_email_recipients')

        # Deleting model 'Sub_val'
        db.delete_table('emailhelper_sub_val')

        # Deleting model 'Val'
        db.delete_table('emailhelper_val')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'competition.founder': {
            'Meta': {'object_name': 'Founder'},
            'birth': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'require_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'emailhelper.bulk_email': {
            'Meta': {'object_name': 'Bulk_email'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_markdown': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competition.Founder']", 'symmetrical': 'False'}),
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
