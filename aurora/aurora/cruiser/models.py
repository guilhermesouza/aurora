from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import datetime

#TODO move it to file?
DEFAULT_IMPORT_BLOCK = "import fabric"


class Project(models.Model):
    """Available projects"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    description = models.CharField(verbose_name=_('description'), max_length=128, null=True, blank=True)
    repository = models.CharField(verbose_name=_('repository'), help_text=_('will be available in recipes as env.repository'), max_length=128)
    import_block = models.TextField(verbose_name=_('import block'), help_text=_('used in fabfile import block'), default=DEFAULT_IMPORT_BLOCK)

    def __unicode__(self):
        return self.name


class ProjectParam(models.Model):
    """Common param for project environment"""
    project = models.ForeignKey(Project, verbose_name=_('project'))
    name = models.CharField(verbose_name=_('name'), max_length=16, help_text=_('env.[name] in recipes'))
    value = models.CharField(verbose_name=_('name'), max_length=128, help_text=_('use " for strings'))

    class Meta:
        unique_together = ("project", "name", "value")

    def __unicode__(self):
        return "%s: %s = %s " % (self.project.name, self.name, self.value)


class Stage(models.Model):
    """Stages for deployment"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    project = models.ForeignKey(Project, verbose_name=_('project'))
    branch = models.CharField(verbose_name=_('branch'), help_text=_('will be available in recipes as env.branch'), max_length=16, null=True, blank=True)
    host = models.CharField(verbose_name=_('branch'), help_text=_('will be available in recipes as env.host'), max_length=64, null=True, blank=True)
    users = models.ManyToManyField(User, verbose_name=_('users'), through='StageUser', related_name=_('users'))
    tasks = models.ManyToManyField('Task', verbose_name=_('tasks'), through='StageTask', related_name=_('tasks'))

    def __unicode__(self):
        return self.name


class StageParam(models.Model):
    """Specified param for stage environment"""
    stage = models.ForeignKey(Stage, verbose_name=_('stage'))
    name = models.CharField(verbose_name=_('name'), max_length=16, help_text=_('env.[name] in recipes'))
    value = models.CharField(verbose_name=_('name'), max_length=128, help_text=_('use " for strings'))

    class Meta:
        unique_together = ("stage", "name", "value")

    def __unicode__(self):
        return "%s: %s = %s " % (self.stage.name, self.name, self.value)


class StageUser(models.Model):
    """User for stage"""
    user = models.ForeignKey(User, verbose_name=_('user'))
    stage = models.ForeignKey(Stage, verbose_name=_('stage'))
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.stage)


class Task(models.Model):
    """Task for fabfile"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    description = models.CharField(verbose_name=_('description'), max_length=128, null=True, blank=True)
    body = models.TextField(verbose_name=_('task body'), help_text=_('task body should include all imports, specified for this task'))

    def __unicode__(self):
        return self.name


class StageTask(models.Model):
    """Task for stage"""
    task = models.ForeignKey(Task, verbose_name=_('task'))
    stage = models.ForeignKey(Stage, verbose_name=_('stage'))
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.stage, self.task)


class Deploy(models.Model):
    """Deploy to stage"""
    FAILED = 'failed'
    RUNNING = 'running'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    STATUS_CHOICES = (
        (RUNNING, _('RUNNING')),
        (COMPLETED, _('COMPLETED')),
        (CANCELED, _('CANCELED')),
        (FAILED, _('FAILED')),
    )

    user = models.ForeignKey(User, verbose_name=_('user'))
    stage = models.ForeignKey(Stage, verbose_name=_('stage'))
    task = models.ForeignKey(Task, verbose_name=_('task'))
    revision = models.CharField(verbose_name=_('revision'), max_length=32)
    started_at = models.DateTimeField(verbose_name=_('started at'))
    finished_at = models.DateTimeField(verbose_name=_('finished at'))
    log = models.TextField(verbose_name=_('log'))
    status = models.IntegerField(verbose_name=_('status'), choices=STATUS_CHOICES)

    def __unicode__(self):
        "%s: %s - %s" % (self.stage, self.task, self.started_at)
