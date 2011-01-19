# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'AnonymousTeamKey'
        db.delete_table('competition_anonymousteamkey')

        # Deleting model 'AnonymousFounderKey'
        db.delete_table('competition_anonymousfounderkey')

        # Adding model 'AnonTeamKey'
        db.create_table('competition_anonteamkey', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Team'], unique=True, null=True)),
        ))
        db.send_create_signal('competition', ['AnonTeamKey'])

        # Adding model 'AnonFounderKey'
        db.create_table('competition_anonfounderkey', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('founder', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Founder'], unique=True, null=True)),
        ))
        db.send_create_signal('competition', ['AnonFounderKey'])


    def backwards(self, orm):
        
        # Adding model 'AnonymousTeamKey'
        db.create_table('competition_anonymousteamkey', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Team'], unique=True, null=True)),
        ))
        db.send_create_signal('competition', ['AnonymousTeamKey'])

        # Adding model 'AnonymousFounderKey'
        db.create_table('competition_anonymousfounderkey', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('founder', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Founder'], unique=True, null=True)),
        ))
        db.send_create_signal('competition', ['AnonymousFounderKey'])

        # Deleting model 'AnonTeamKey'
        db.delete_table('competition_anonteamkey')

        # Deleting model 'AnonFounderKey'
        db.delete_table('competition_anonfounderkey')


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
        'competition.anonfounderkey': {
            'Meta': {'object_name': 'AnonFounderKey'},
            'founder': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Founder']", 'unique': 'True', 'null': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'competition.anonteamkey': {
            'Meta': {'object_name': 'AnonTeamKey'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Team']", 'unique': 'True', 'null': 'True'})
        },
        'competition.applicationrequirements': {
            'Meta': {'object_name': 'ApplicationRequirements'},
            'applicant_types': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comp_applicant_types'", 'symmetrical': 'False', 'to': "orm['utils.Tag']"}),
            'business_types': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comp_business_types'", 'symmetrical': 'False', 'to': "orm['utils.Tag']"}),
            'competition': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Competition']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institutions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comp_institutions'", 'symmetrical': 'False', 'to': "orm['utils.Tag']"}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comp_locations'", 'symmetrical': 'False', 'to': "orm['utils.Tag']"}),
            'other_requirements': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comp_other_requirements'", 'symmetrical': 'False', 'to': "orm['utils.Tag']"})
        },
        'competition.competition': {
            'Meta': {'object_name': 'Competition'},
            'applicants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'competitions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['competition.Founder']"}),
            'current_phase': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'competition_unused'", 'unique': 'True', 'null': 'True', 'to': "orm['competition.Phase']"}),
            'hosted_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'template_base': ('django.db.models.fields.CharField', [], {'default': "'base.html'", 'max_length': '200'}),
            'template_pitch': ('django.db.models.fields.CharField', [], {'default': "'entercompetition/pitch_form.html'", 'max_length': '201'}),
            'template_stylesheet': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'competition.extrafounderinfo': {
            'Meta': {'object_name': 'ExtraFounderInfo'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'founder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extra_info'", 'to': "orm['competition.Founder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.ExtraFounderQuestion']"})
        },
        'competition.extrafounderquestion': {
            'Meta': {'object_name': 'ExtraFounderQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'raw_choices': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'competition.founder': {
            'Meta': {'object_name': 'Founder'},
            'birth': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'require_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'competition.phase': {
            'Meta': {'object_name': 'Phase'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_phases'", 'to': "orm['competition.Competition']"}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 18, 21, 36, 22, 809903)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_judging_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'min_judgements_per_pitch': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140', 'blank': 'True'}),
            'pitch_type': ('django.db.models.fields.CharField', [], {'default': "'online'", 'max_length': '20'})
        },
        'competition.phasesetupsteps': {
            'Meta': {'object_name': 'PhaseSetupSteps'},
            'announced_applications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'announced_judging_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'application_setup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'details_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_judges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phase': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Phase']", 'unique': 'True'}),
            'selected_winners': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        'competition.pitchfile': {
            'Meta': {'object_name': 'PitchFile'},
            'file_location': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pitch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['competition.Pitch']"}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.PitchUpload']"})
        },
        'competition.pitchquestion': {
            'Meta': {'ordering': "['order']", 'object_name': 'PitchQuestion'},
            'field_rows': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'competition.pitchupload': {
            'Meta': {'ordering': "['id']", 'object_name': 'PitchUpload'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"}),
            'prompt': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'competition.scribdfiledata': {
            'Meta': {'object_name': 'ScribdFileData'},
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'doc_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pitch_file': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'scribd_file_data'", 'unique': 'True', 'to': "orm['competition.PitchFile']"}),
            'secret_password': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'competition.team': {
            'Meta': {'object_name': 'Team'},
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
        'utils.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['competition']
