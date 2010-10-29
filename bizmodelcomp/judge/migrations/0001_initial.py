# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'JudgeInvitation'
        db.create_table('judge_judgeinvitation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('this_phase_only', self.gf('django.db.models.fields.related.ForeignKey')(related_name='judge_invitations', to=orm['competition.Phase'])),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='judge_invitations', to=orm['competition.Competition'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('judge', ['JudgeInvitation'])

        # Adding model 'Judge'
        db.create_table('judge_judge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_judging_all_phases', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('judge', ['Judge'])

        # Adding M2M table for field phases on 'Judge'
        db.create_table('judge_judge_phases', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('judge', models.ForeignKey(orm['judge.judge'], null=False)),
            ('phase', models.ForeignKey(orm['competition.phase'], null=False))
        ))
        db.create_unique('judge_judge_phases', ['judge_id', 'phase_id'])


    def backwards(self, orm):
        
        # Deleting model 'JudgeInvitation'
        db.delete_table('judge_judgeinvitation')

        # Deleting model 'Judge'
        db.delete_table('judge_judge')

        # Removing M2M table for field phases on 'Judge'
        db.delete_table('judge_judge_phases')


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
        'competition.competition': {
            'Meta': {'object_name': 'Competition'},
            'applicants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'competitions'", 'blank': 'True', 'null': 'True', 'to': "orm['competition.Founder']"}),
            'hosted_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'template_base': ('django.db.models.fields.CharField', [], {'default': "'base.html'", 'max_length': '200'}),
            'template_pitch': ('django.db.models.fields.CharField', [], {'default': "'entercompetition/pitch_form.html'", 'max_length': '201'}),
            'template_stylesheet': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
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
        'competition.phase': {
            'Meta': {'object_name': 'Phase'},
            'applications_close_judging_open': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'applications_open': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judging_close': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'judge.judge': {
            'Meta': {'object_name': 'Judge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_judging_all_phases': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phases': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'judges'", 'symmetrical': 'False', 'to': "orm['competition.Phase']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'judge.judgeinvitation': {
            'Meta': {'object_name': 'JudgeInvitation'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judge_invitations'", 'to': "orm['competition.Competition']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'this_phase_only': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judge_invitations'", 'to': "orm['competition.Phase']"})
        }
    }

    complete_apps = ['judge']
