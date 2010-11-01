# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'JudgedAnswer'
        db.create_table('judge_judgedanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('judged_pitch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['judge.JudgedPitch'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.PitchAnswer'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('feedback', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal('judge', ['JudgedAnswer'])

        # Adding model 'JudgedPitch'
        db.create_table('judge_judgedpitch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pitch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='judgements', to=orm['competition.Pitch'])),
            ('judge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='judgements', to=orm['judge.JudgeInvitation'])),
            ('feedback', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
        ))
        db.send_create_signal('judge', ['JudgedPitch'])


    def backwards(self, orm):
        
        # Deleting model 'JudgedAnswer'
        db.delete_table('judge_judgedanswer')

        # Deleting model 'JudgedPitch'
        db.delete_table('judge_judgedpitch')


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
            'is_judging_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'judging_close': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'competition.pitch': {
            'Meta': {'object_name': 'Pitch'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Founder']"}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"})
        },
        'competition.pitchanswer': {
            'Meta': {'object_name': 'PitchAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pitch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['competition.Pitch']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.PitchQuestion']"})
        },
        'competition.pitchquestion': {
            'Meta': {'ordering': "['order']", 'object_name': 'PitchQuestion'},
            'field_rows': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'order': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '4', 'decimal_places': '2'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"}),
            'prompt': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'raw_choices': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'judge.judgedanswer': {
            'Meta': {'object_name': 'JudgedAnswer'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.PitchAnswer']"}),
            'feedback': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judged_pitch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['judge.JudgedPitch']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'judge.judgedpitch': {
            'Meta': {'object_name': 'JudgedPitch'},
            'feedback': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judgements'", 'to': "orm['judge.JudgeInvitation']"}),
            'pitch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judgements'", 'to': "orm['competition.Pitch']"})
        },
        'judge.judgeinvitation': {
            'Meta': {'object_name': 'JudgeInvitation'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judge_invitations'", 'to': "orm['competition.Competition']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'has_received_invite_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_phase_judging_open_emails_from': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sent_judging_open_emails_to'", 'symmetrical': 'False', 'to': "orm['competition.Phase']"}),
            'this_phase_only': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judge_invitations'", 'blank': 'True', 'null': 'True', 'to': "orm['competition.Phase']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['judge']
