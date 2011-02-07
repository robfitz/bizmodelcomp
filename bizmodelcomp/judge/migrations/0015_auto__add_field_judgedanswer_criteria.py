# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'JudgedAnswer.criteria'
        db.add_column('judge_judgedanswer', 'criteria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['judge.JudgingCriteria'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'JudgedAnswer.criteria'
        db.delete_column('judge_judgedanswer', 'criteria_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'competition.competition': {
            'Meta': {'object_name': 'Competition'},
            'applicants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'competitions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['competition.Founder']"}),
            'current_phase': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'competition_unused'", 'unique': 'True', 'null': 'True', 'to': "orm['competition.Phase']"}),
            'hex_color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'hex_header_color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'hosted_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'template_base': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'template_pitch': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '201', 'blank': 'True'}),
            'template_stylesheet': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'terms_of_service': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10000', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'competition.founder': {
            'Meta': {'object_name': 'Founder'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'applicant_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'founder_applicant_type'", 'null': 'True', 'to': "orm['utils.Tag']"}),
            'birth': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'course_of_study': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'founder_institution'", 'null': 'True', 'to': "orm['utils.Tag']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'founder_location'", 'null': 'True', 'to': "orm['utils.Tag']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'require_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'year_of_study': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'competition.phase': {
            'Meta': {'object_name': 'Phase'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_phases'", 'to': "orm['competition.Competition']"}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 4, 12, 18, 34, 506734)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_judging_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'min_judgements_per_pitch': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140', 'blank': 'True'}),
            'pitch_type': ('django.db.models.fields.CharField', [], {'default': "'online'", 'max_length': '20'}),
            'scoring_tooltip': ('django.db.models.fields.CharField', [], {'default': "'0 points means a completely missing or invalid answer. 1 point is an attempted but very bad answer. Maximum points means you would be pleased to see this answer in a professional pitch.'", 'max_length': '500', 'blank': 'True'})
        },
        'competition.pitch': {
            'Meta': {'ordering': "['order', '-created']", 'object_name': 'Pitch'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Founder']", 'null': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Team']", 'null': 'True'})
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
            'extra_info': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'field_rows': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_divider': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hidden_from_applicants': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'judge_feedback_prompt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140'}),
            'judge_points_prompt': ('django.db.models.fields.CharField', [], {'default': "'Low scores are bad, high scores are great'", 'max_length': '140'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'order': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '4', 'decimal_places': '2'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"}),
            'prompt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'raw_choices': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000', 'blank': 'True'})
        },
        'competition.team': {
            'Meta': {'object_name': 'Team'},
            'business_types': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'team_business_types'", 'symmetrical': 'False', 'to': "orm['utils.Tag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': "'140'", 'blank': 'True'}),
            'other_members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competition.Founder']", 'symmetrical': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_set'", 'to': "orm['competition.Founder']"})
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
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.PitchAnswer']", 'null': 'True', 'blank': 'True'}),
            'criteria': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['judge.JudgingCriteria']", 'null': 'True', 'blank': 'True'}),
            'feedback': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judged_pitch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['judge.JudgedPitch']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'judge.judgedpitch': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'JudgedPitch'},
            'feedback': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judgements'", 'to': "orm['judge.JudgeInvitation']"}),
            'max_overall_score': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'overall_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pitch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judgements'", 'to': "orm['competition.Pitch']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'judge.judgeinvitation': {
            'Meta': {'object_name': 'JudgeInvitation'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'judge_invitations'", 'to': "orm['competition.Competition']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'has_received_invite_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_phase_judging_open_emails_from': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sent_judging_open_emails_to'", 'symmetrical': 'False', 'to': "orm['competition.Phase']"}),
            'this_phase_only': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'judge_invitations'", 'null': 'True', 'to': "orm['competition.Phase']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'judge.judgingcriteria': {
            'Meta': {'object_name': 'JudgingCriteria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_text_feedback': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'order': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '4', 'decimal_places': '2'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']", 'null': 'True'}),
            'prompt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'scoring_tooltip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'utils.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['judge']
