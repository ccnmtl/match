# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DiscussionTopic'
        db.create_table('nutrition_discussiontopic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('estimated_time', self.gf('django.db.models.fields.IntegerField')()),
            ('reply', self.gf('django.db.models.fields.TextField')()),
            ('actual_time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('nutrition', ['DiscussionTopic'])

        # Adding model 'CounselingSession'
        db.create_table('nutrition_counselingsession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('available_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('nutrition', ['CounselingSession'])

        # Adding M2M table for field topics on 'CounselingSession'
        db.create_table('nutrition_counselingsession_topics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('counselingsession', models.ForeignKey(orm['nutrition.counselingsession'], null=False)),
            ('discussiontopic', models.ForeignKey(orm['nutrition.discussiontopic'], null=False))
        ))
        db.create_unique('nutrition_counselingsession_topics', ['counselingsession_id', 'discussiontopic_id'])

        # Adding model 'CounselingSessionState'
        db.create_table('nutrition_counselingsessionstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nutrition_discussion_user', to=orm['auth.User'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nutrition.CounselingSession'])),
            ('elapsed_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('nutrition', ['CounselingSessionState'])

        # Adding M2M table for field answered on 'CounselingSessionState'
        db.create_table('nutrition_counselingsessionstate_answered', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('counselingsessionstate', models.ForeignKey(orm['nutrition.counselingsessionstate'], null=False)),
            ('discussiontopic', models.ForeignKey(orm['nutrition.discussiontopic'], null=False))
        ))
        db.create_unique('nutrition_counselingsessionstate_answered', ['counselingsessionstate_id', 'discussiontopic_id'])


    def backwards(self, orm):
        
        # Deleting model 'DiscussionTopic'
        db.delete_table('nutrition_discussiontopic')

        # Deleting model 'CounselingSession'
        db.delete_table('nutrition_counselingsession')

        # Removing M2M table for field topics on 'CounselingSession'
        db.delete_table('nutrition_counselingsession_topics')

        # Deleting model 'CounselingSessionState'
        db.delete_table('nutrition_counselingsessionstate')

        # Removing M2M table for field answered on 'CounselingSessionState'
        db.delete_table('nutrition_counselingsessionstate_answered')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nutrition.counselingsession': {
            'Meta': {'object_name': 'CounselingSession'},
            'available_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nutrition.DiscussionTopic']", 'symmetrical': 'False'})
        },
        'nutrition.counselingsessionstate': {
            'Meta': {'object_name': 'CounselingSessionState'},
            'answered': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['nutrition.DiscussionTopic']", 'null': 'True', 'blank': 'True'}),
            'elapsed_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.CounselingSession']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nutrition_discussion_user'", 'to': "orm['auth.User']"})
        },
        'nutrition.discussiontopic': {
            'Meta': {'object_name': 'DiscussionTopic'},
            'actual_time': ('django.db.models.fields.IntegerField', [], {}),
            'estimated_time': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reply': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'pagetree.pageblock': {
            'Meta': {'ordering': "('section', 'ordinality')", 'object_name': 'PageBlock'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'css_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Hierarchy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['nutrition']
