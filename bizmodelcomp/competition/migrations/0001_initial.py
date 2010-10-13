# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Founder'
        db.create_table('competition_founder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('birth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('competition', ['Founder'])

        # Adding model 'AnonymousFounderKey'
        db.create_table('competition_anonymousfounderkey', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('founder', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Founder'], unique=True)),
        ))
        db.send_create_signal('competition', ['AnonymousFounderKey'])

        # Adding model 'Competition'
        db.create_table('competition_competition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('competition', ['Competition'])

        # Adding M2M table for field applicants on 'Competition'
        db.create_table('competition_competition_applicants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('competition', models.ForeignKey(orm['competition.competition'], null=False)),
            ('founder', models.ForeignKey(orm['competition.founder'], null=False))
        ))
        db.create_unique('competition_competition_applicants', ['competition_id', 'founder_id'])

        # Adding model 'CompetitionCopyTemplate'
        db.create_table('competition_competitioncopytemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('tooltip', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('default_text', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('competition', ['CompetitionCopyTemplate'])

        # Adding model 'CompetitionCopy'
        db.create_table('competition_competitioncopy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Competition'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('competition', ['CompetitionCopy'])

        # Adding model 'Phase'
        db.create_table('competition_phase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Competition'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
        ))
        db.send_create_signal('competition', ['Phase'])

        # Adding model 'Pitch'
        db.create_table('competition_pitch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Founder'])),
            ('phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Phase'])),
        ))
        db.send_create_signal('competition', ['Pitch'])

        # Adding model 'PitchQuestion'
        db.create_table('competition_pitchquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Phase'])),
            ('prompt', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('raw_choices', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
        ))
        db.send_create_signal('competition', ['PitchQuestion'])

        # Adding model 'PitchAnswer'
        db.create_table('competition_pitchanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.PitchQuestion'])),
            ('pitch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Pitch'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('competition', ['PitchAnswer'])

        # Adding model 'PitchUpload'
        db.create_table('competition_pitchupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Phase'])),
            ('prompt', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('competition', ['PitchUpload'])

        # Adding model 'PitchFile'
        db.create_table('competition_pitchfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upload', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.PitchUpload'])),
            ('pitch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Pitch'])),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('competition', ['PitchFile'])

        # Adding model 'ExtraFounderQuestion'
        db.create_table('competition_extrafounderquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prompt', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('raw_choices', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('competition', ['ExtraFounderQuestion'])

        # Adding model 'ExtraFounderInfo'
        db.create_table('competition_extrafounderinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.ExtraFounderQuestion'])),
            ('founder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='extra_info', to=orm['competition.Founder'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=5000)),
        ))
        db.send_create_signal('competition', ['ExtraFounderInfo'])


    def backwards(self, orm):
        
        # Deleting model 'Founder'
        db.delete_table('competition_founder')

        # Deleting model 'AnonymousFounderKey'
        db.delete_table('competition_anonymousfounderkey')

        # Deleting model 'Competition'
        db.delete_table('competition_competition')

        # Removing M2M table for field applicants on 'Competition'
        db.delete_table('competition_competition_applicants')

        # Deleting model 'CompetitionCopyTemplate'
        db.delete_table('competition_competitioncopytemplate')

        # Deleting model 'CompetitionCopy'
        db.delete_table('competition_competitioncopy')

        # Deleting model 'Phase'
        db.delete_table('competition_phase')

        # Deleting model 'Pitch'
        db.delete_table('competition_pitch')

        # Deleting model 'PitchQuestion'
        db.delete_table('competition_pitchquestion')

        # Deleting model 'PitchAnswer'
        db.delete_table('competition_pitchanswer')

        # Deleting model 'PitchUpload'
        db.delete_table('competition_pitchupload')

        # Deleting model 'PitchFile'
        db.delete_table('competition_pitchfile')

        # Deleting model 'ExtraFounderQuestion'
        db.delete_table('competition_extrafounderquestion')

        # Deleting model 'ExtraFounderInfo'
        db.delete_table('competition_extrafounderinfo')


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
        'competition.anonymousfounderkey': {
            'Meta': {'object_name': 'AnonymousFounderKey'},
            'founder': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Founder']", 'unique': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'competition.competition': {
            'Meta': {'object_name': 'Competition'},
            'applicants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'competitions'", 'symmetrical': 'False', 'to': "orm['competition.Founder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'competition.competitioncopy': {
            'Meta': {'object_name': 'CompetitionCopy'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'})
        },
        'competition.competitioncopytemplate': {
            'Meta': {'object_name': 'CompetitionCopyTemplate'},
            'default_text': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tooltip': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
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
            'birth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'competition.phase': {
            'Meta': {'object_name': 'Phase'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'competition.pitch': {
            'Meta': {'object_name': 'Pitch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Founder']"}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"})
        },
        'competition.pitchanswer': {
            'Meta': {'object_name': 'PitchAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pitch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Pitch']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.PitchQuestion']"})
        },
        'competition.pitchfile': {
            'Meta': {'object_name': 'PitchFile'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pitch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Pitch']"}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.PitchUpload']"})
        },
        'competition.pitchquestion': {
            'Meta': {'object_name': 'PitchQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"}),
            'prompt': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'raw_choices': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'})
        },
        'competition.pitchupload': {
            'Meta': {'object_name': 'PitchUpload'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Phase']"}),
            'prompt': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['competition']
