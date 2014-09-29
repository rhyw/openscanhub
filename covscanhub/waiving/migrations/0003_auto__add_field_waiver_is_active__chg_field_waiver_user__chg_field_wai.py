# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Waiver.is_active'
        db.add_column(u'waiving_waiver', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Waiver.user'
        db.alter_column(u'waiving_waiver', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.LongnameUser']))

        # Changing field 'Waiver.date'
        db.alter_column(u'waiving_waiver', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'WaivingLog.date'
        db.alter_column(u'waiving_waivinglog', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'WaivingLog.user'
        db.alter_column(u'waiving_waivinglog', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.LongnameUser']))

    def backwards(self, orm):
        # Deleting field 'Waiver.is_active'
        db.delete_column(u'waiving_waiver', 'is_active')


        # Changing field 'Waiver.user'
        db.alter_column(u'waiving_waiver', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Waiver.date'
        db.alter_column(u'waiving_waiver', 'date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'WaivingLog.date'
        db.alter_column(u'waiving_waivinglog', 'date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'WaivingLog.user'
        db.alter_column(u'waiving_waivinglog', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.longnameuser': {
            'Meta': {'object_name': 'LongnameUser', 'db_table': "'auth_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'scan.package': {
            'Meta': {'object_name': 'Package'},
            'blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'eligible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'scan.systemrelease': {
            'Meta': {'object_name': 'SystemRelease'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['scan.SystemRelease']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'release': ('django.db.models.fields.IntegerField', [], {}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'waiving.bugzilla': {
            'Meta': {'object_name': 'Bugzilla'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scan.Package']"}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scan.SystemRelease']"})
        },
        u'waiving.checker': {
            'Meta': {'object_name': 'Checker'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.CheckerGroup']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'severity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'waiving.checkergroup': {
            'Meta': {'object_name': 'CheckerGroup'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'waiving.defect': {
            'Meta': {'object_name': 'Defect'},
            'annotation': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'checker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.Checker']"}),
            'cwe': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'defect_identifier': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'events': ('kobo.django.fields.JSONField', [], {'default': '[]'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_event': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'result_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.ResultGroup']"}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'})
        },
        u'waiving.result': {
            'Meta': {'object_name': 'Result'},
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scanner': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'scanner_version': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'scanning_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'waiving.resultgroup': {
            'Meta': {'object_name': 'ResultGroup'},
            'checker_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.CheckerGroup']"}),
            'defect_type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'}),
            'defects_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.Result']"}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '4'})
        },
        u'waiving.waiver': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Waiver'},
            'bz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.Bugzilla']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'result_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.ResultGroup']"}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.LongnameUser']"})
        },
        u'waiving.waivinglog': {
            'Meta': {'ordering': "['date']", 'object_name': 'WaivingLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.LongnameUser']"}),
            'waiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waiving.Waiver']"})
        }
    }

    complete_apps = ['waiving']