from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

import datetime

#TODO move it to file?
DEFAULT_IMPORT_BLOCK = "import fabric"

def present(val):
    return all([val != None, str(val).strip() != ''])

class Project(models.Model):
    """Available projects"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    description = models.CharField(verbose_name=_('description'), max_length=128, null=True, blank=True)
    repository = models.CharField(verbose_name=_('repository'), help_text=_('will be available in recipes as env.repository'), max_length=128)
    import_block = models.TextField(verbose_name=_('import block'), help_text=_('used in fabfile import block'), default=DEFAULT_IMPORT_BLOCK)

    def __unicode__(self):
        return self.name

    def params(self):
        """Rerun dict of project params"""
        params = {}
        if present(self.repository):
            params['repository'] = self.repository

        return params.update(dict((x.name, x.value) for x in self.projectparam_set.all()))


class ProjectParam(models.Model):
    """Common param for project environment"""
    project = models.ForeignKey(Project, verbose_name=_('project'))
    name = models.CharField(verbose_name=_('name'), max_length=16, help_text=_('env.[name] in recipes'))
    value = models.CharField(verbose_name=_('name'), max_length=128, help_text=_('use " for strings'))

    class Meta:
        unique_together = ("project", "name", "value")

    def __unicode__(self):
        return "%s: %s = %s " % (self.project.name, self.name, self.value)

    def get_change_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def get_delete_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_delete" % (content_type.app_label, content_type.model), args=(self.id,))

    def to_param(self):
        """Return dict {name:value}"""
        return dict([[self.name, self.value]])


class Stage(models.Model):
    """Stages for deployment"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    project = models.ForeignKey(Project, verbose_name=_('project'))
    branch = models.CharField(verbose_name=_('branch'), help_text=_('will be available in recipes as env.branch'), max_length=16, null=True, blank=True)
    host = models.CharField(verbose_name=_('host'), help_text=_('will be available in recipes as env.host'), max_length=64, null=True, blank=True)
    users = models.ManyToManyField(User, verbose_name=_('users'), through='StageUser', related_name=_('users'))
    tasks = models.ManyToManyField('Task', verbose_name=_('tasks'), through='StageTask', related_name=_('tasks'))

    def __unicode__(self):
        return "%s: %s" % (self.project, self.name)

    def params(self):
        """Rerun list of project params"""
        params = {}
        if present(self.host):
            params['host'] = self.host

        if present(self.branch):
            params['branch'] = self.branch

        return params.update(dict((x.name, x.value) for x in self.stageparam_set.all()))

    def usage_tasks(self):
        """List of tasks"""
        return [task.body for task in self.tasks.all()]

    def dep_count(self):
        """deployments count for given stage"""
        return None #2do

class StageParam(models.Model):
    """Specified param for stage environment"""
    stage = models.ForeignKey(Stage, verbose_name=_('stage'))
    name = models.CharField(verbose_name=_('name'), max_length=16, help_text=_('env.[name] in recipes'))
    value = models.CharField(verbose_name=_('value'), max_length=128, help_text=_('use " for strings'))

    class Meta:
        unique_together = ("stage", "name", "value")

    def __unicode__(self):
        return "%s: %s = %s " % (self.stage.name, self.name, self.value)

    def to_param(self):
        """Return dict {name:value}"""
        return dict([[self.name, self.value]])


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
    READY = 'ready'
    STATUS_CHOICES = (
        (READY, _('READY')),
        (RUNNING, _('RUNNING')),
        (COMPLETED, _('COMPLETED')),
        (CANCELED, _('CANCELED')),
        (FAILED, _('FAILED')),
    )
    # CSS classes from Twi Bootstrap http://twitter.github.com/bootstrap/components.html#typography
    STATUS_CSS = {
        READY: '',
        RUNNING: 'alert-info',
        COMPLETED: 'alert-success',
        CANCELED: 'alert-error',
        FAILED: 'alert-error',
    }

    user = models.ForeignKey(User, verbose_name=_('user'))
    stage = models.ForeignKey(Stage, verbose_name=_('stage'))
    task = models.ForeignKey(Task, verbose_name=_('task'))
    revision = models.CharField(verbose_name=_('revision'), max_length=32)
    started_at = models.DateTimeField(verbose_name=_('started at'), null=True)
    finished_at = models.DateTimeField(verbose_name=_('finished at'), null=True)
    log = models.TextField(verbose_name=_('log'), default="")
    status = models.CharField(verbose_name=_('status'), max_length=16, choices=STATUS_CHOICES, default=READY)
    branch = models.CharField(verbose_name=_('branch'), max_length=16, null=True, blank=True)

    def __unicode__(self):
        return "%s: %s - %s" % (self.stage, self.task, self.started_at)

    def run(self):
        """Run deploy"""
        if not self.ready():
            return False

        self.started_at = datetime.datetime.now()
        self.status = RUNNING
        self.save()

        #do_something

        self.finished_at = datetime.datetime.now()
        self.status = COMPLETED
        self.save()

    def ready(self):
        """Ready for run"""
        return RUNNING == self.status

    def build_fabfile(self):
        """Generate fabfile and save to fs"""
        from aurora.cruiser.lib.fabfile import Fabfile

        fabfile = Fabfile(self.stage.project.import_block,
                          self.stage.usage_tasks(),
                          self.fabfile_path(),
                          self.env_params())

        fabfile.build()

    def fabfile_path(self):
        """Path to file"""
        return '%s/deploy_%s/' % (settings.FABFILE_DIR, self.id)

    def env_params(self):
        """Get params for current deployment"""
        params = self.stage.project.params()
        params.update(self.stage.params())
        if present(self.branch):
            params.update({'branch': self.branch})

        return params

    def css(self):
        return self.STATUS_CSS[self.status]
