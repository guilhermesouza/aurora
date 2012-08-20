# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('cruiser_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('repository', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('import_block', self.gf('django.db.models.fields.TextField')(default='import fabric')),
        ))
        db.send_create_signal('cruiser', ['Project'])

        # Adding model 'ProjectParam'
        db.create_table('cruiser_projectparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('cruiser', ['ProjectParam'])

        # Adding unique constraint on 'ProjectParam', fields ['project', 'name', 'value']
        db.create_unique('cruiser_projectparam', ['project_id', 'name', 'value'])

        # Adding model 'Stage'
        db.create_table('cruiser_stage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Project'])),
            ('branch', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('cruiser', ['Stage'])

        # Adding model 'StageParam'
        db.create_table('cruiser_stageparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Stage'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('cruiser', ['StageParam'])

        # Adding unique constraint on 'StageParam', fields ['stage', 'name', 'value']
        db.create_unique('cruiser_stageparam', ['stage_id', 'name', 'value'])

        # Adding model 'StageUser'
        db.create_table('cruiser_stageuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Stage'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('cruiser', ['StageUser'])

        # Adding model 'Task'
        db.create_table('cruiser_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cruiser', ['Task'])

        # Adding model 'StageTask'
        db.create_table('cruiser_stagetask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Task'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Stage'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('cruiser', ['StageTask'])

        # Adding model 'Deploy'
        db.create_table('cruiser_deploy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Stage'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cruiser.Task'])),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('finished_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('log', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cruiser', ['Deploy'])


    def backwards(self, orm):
        # Removing unique constraint on 'StageParam', fields ['stage', 'name', 'value']
        db.delete_unique('cruiser_stageparam', ['stage_id', 'name', 'value'])

        # Removing unique constraint on 'ProjectParam', fields ['project', 'name', 'value']
        db.delete_unique('cruiser_projectparam', ['project_id', 'name', 'value'])

        # Deleting model 'Project'
        db.delete_table('cruiser_project')

        # Deleting model 'ProjectParam'
        db.delete_table('cruiser_projectparam')

        # Deleting model 'Stage'
        db.delete_table('cruiser_stage')

        # Deleting model 'StageParam'
        db.delete_table('cruiser_stageparam')

        # Deleting model 'StageUser'
        db.delete_table('cruiser_stageuser')

        # Deleting model 'Task'
        db.delete_table('cruiser_task')

        # Deleting model 'StageTask'
        db.delete_table('cruiser_stagetask')

        # Deleting model 'Deploy'
        db.delete_table('cruiser_deploy')


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
        'cruiser.deploy': {
            'Meta': {'object_name': 'Deploy'},
            'finished_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cruiser.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_block': ('django.db.models.fields.TextField', [], {'default': "'import fabric'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'repository': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'cruiser.projectparam': {
            'Meta': {'unique_together': "(('project', 'name', 'value'),)", 'object_name': 'ProjectParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Project']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'cruiser.stage': {
            'Meta': {'object_name': 'Stage'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Project']"}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'tasks'", 'symmetrical': 'False', 'through': "orm['cruiser.StageTask']", 'to': "orm['cruiser.Task']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'users'", 'symmetrical': 'False', 'through': "orm['cruiser.StageUser']", 'to': "orm['auth.User']"})
        },
        'cruiser.stageparam': {
            'Meta': {'unique_together': "(('stage', 'name', 'value'),)", 'object_name': 'StageParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'cruiser.stagetask': {
            'Meta': {'object_name': 'StageTask'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Task']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'cruiser.stageuser': {
            'Meta': {'object_name': 'StageUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cruiser.task': {
            'Meta': {'object_name': 'Task'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['cruiser']