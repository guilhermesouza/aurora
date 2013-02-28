from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import signals
from validators import validate_presence

import datetime

#TODO move it to file?
DEFAULT_IMPORT_BLOCK = """from fabric.api import *
from fabric.operations import *
from fabric.decorators import *"""


def present(val):
    return all([val is not None, str(val).strip() != ''])


class ModelWithAdminUrl(models.Model):
    """Model with admin urls"""
    class Meta:
        abstract = True

    def get_add_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_add" % (content_type.app_label, content_type.model))

    def get_change_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def get_delete_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_delete" % (content_type.app_label, content_type.model), args=(self.id,))


class Project(ModelWithAdminUrl):
    """Available projects"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    description = models.CharField(verbose_name=_('description'), max_length=128, null=True, blank=True)
    repository = models.CharField(verbose_name=_('repository'), help_text=_('will be available in recipes as env.repository'), max_length=128, blank=True)
    import_block = models.TextField(verbose_name=_('import block'), help_text=_('used in fabfile import block'), default=DEFAULT_IMPORT_BLOCK)

    def __unicode__(self):
        return self.name

    def prepare_data(self):
        self.repository = self.repository.strip()

    def params(self):
        """Rerun dict of project params"""
        params = {}
        if present(self.repository):
            params['repository'] = "'%s'" % self.repository

        params.update(dict((x.name, x.value) for x in self.projectparam_set.all()))

        return params

    def dep_count(self):
        """deployments count for project"""
        return Deploy.objects.filter(stage__project_id=self.id).count()


class ProjectParam(ModelWithAdminUrl):
    """Common param for project environment"""
    project = models.ForeignKey(Project, verbose_name=_('project'))
    name = models.CharField(verbose_name=_('name'), max_length=16, validators=[validate_presence], help_text=_('env.[name] in recipes'))
    value = models.CharField(verbose_name=_('value'), max_length=128, validators=[validate_presence], help_text=_('use " for strings'))

    class Meta:
        unique_together = ("project", "name", "value")

    def __unicode__(self):
        return "%s: %s = %s " % (self.project.name, self.name, self.value)

    def prepare_data(self):
        if self.name:
            self.name = self.name.strip()
        if self.value:
            self.value = self.value.strip()

    def to_param(self):
        """Return dict {name:value}"""
        return dict([[self.name, self.value]])


class Stage(ModelWithAdminUrl):
    """Stages for deployment"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    project = models.ForeignKey(Project, verbose_name=_('project'), related_name=_('stages'))
    branch = models.CharField(verbose_name=_('branch'), help_text=_('will be available in recipes as env.branch'), max_length=16, null=True, blank=True)
    hosts = models.CharField(verbose_name=_('hosts'), help_text=_('will be available in recipes as env.hosts'), max_length=64, null=True, blank=True)
    users = models.ManyToManyField(User, verbose_name=_('users'), through='StageUser', related_name=_('users'))
    tasks = models.ManyToManyField('Task', verbose_name=_('tasks'), through='StageTask', related_name=_('tasks'))

    def __unicode__(self):
        return "%s: %s" % (self.project, self.name)

    def prepare_data(self):
        if self.branch:
            self.branch = self.branch.strip()
        if self.hosts:
            self.hosts = self.hosts.strip()

    def params(self):
        """Rerun list of project params"""
        params = {}
        if present(self.hosts):
            params['hosts'] = self.hosts

        if present(self.branch):
            params['branch'] = "'%s'" % self.branch

        params.update(dict((x.name, x.value) for x in self.stageparam_set.all()))

        return params

    def usage_tasks(self):
        """List of tasks"""
        return [task.body for task in self.tasks.all()]

    def dep_count(self):
        """deployments count for stage"""
        return Deploy.objects.filter(stage_id=self.id).count()

    def already_deploying(self):
        """Rrturn true if stage deploying now"""
        return self.deploy_set.filter(status=Deploy.RUNNING).count() > 0

    def permitted_for(self, user):
        """Check user permissions"""
        return user in self.users.all()


class StageParam(ModelWithAdminUrl):
    """Specified param for stage environment"""
    stage = models.ForeignKey(Stage, verbose_name=_('stage'))
    name = models.CharField(verbose_name=_('name'), max_length=16, validators=[validate_presence], help_text=_('env.[name] in recipes'))
    value = models.CharField(verbose_name=_('value'), max_length=128, validators=[validate_presence], help_text=_('use " for strings'))

    class Meta:
        unique_together = ("stage", "name", "value")

    def __unicode__(self):
        return "%s: %s = %s " % (self.stage.name, self.name, self.value)

    def prepare_data(self):
        self.name = self.name.strip()
        self.value = self.value.strip()

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


class Task(ModelWithAdminUrl):
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
    revision = models.CharField(verbose_name=_('revision'), max_length=32, blank=True)
    started_at = models.DateTimeField(verbose_name=_('started at'), null=True)
    finished_at = models.DateTimeField(verbose_name=_('finished at'), null=True)
    log = models.TextField(verbose_name=_('log'), default="")
    status = models.CharField(verbose_name=_('status'), max_length=16, choices=STATUS_CHOICES, default=READY)
    branch = models.CharField(verbose_name=_('branch'), max_length=16, null=True, blank=True, default='')
    comment = models.CharField(verbose_name=_('comment'), max_length=128, null=True, blank=True)

    def __unicode__(self):
        return "%s: %s - %s" % (self.stage, self.task, self.started_at)

    def prepare_data(self):
        self.branch = self.branch.strip()

    def run(self):
        """Run deploy"""
        if not self.ready():
            return False

        self.started_at = datetime.datetime.now()
        self.status = self.RUNNING
        self.save()
        return True

    def ready(self):
        """Ready for run"""
        return self.READY == self.status

    def running(self):
        """Running this time"""
        return self.RUNNING == self.status

    def build_fabfile(self):
        """Generate fabfile and save to fs"""
        from aurora.cruiser.lib.fabfile import Fabfile

        fabfile = Fabfile(self.stage.project.import_block,
                          self.stage.usage_tasks(),
                          self.working_path(),
                          self.env_params())

        fabfile.build()

    def working_path(self):
        """Path to file"""
        return '%sdeploy_%s/' % (settings.FABFILE_DIR, self.id)

    def env_params(self):
        """Get params for current deployment"""
        params = self.stage.project.params()
        params.update(self.stage.params())
        if present(self.branch):
            params.update({'branch': "'%s'" % self.branch})

        return params

    def css(self):
        return self.STATUS_CSS[self.status]

    def get_log(self):
        """Get log from output file or from base"""
        if self.running():
            with open('%soutput.log' % self.working_path(), 'r') as f:
                log = ''.join(f.readlines())
        else:
            log = self.log

        return log

    def finish_with_status(self, status):
        """Mark as finished"""
        self.log = self.get_log()
        self.status = status
        self.finished_at = datetime.datetime.now()
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('deployment_monitor', (), {'deploy_id': self.id})

    def get_status_from_log(self):
        log = self.get_log()
        last_row = log.strip('\n').split('\n')[-1]

        if 'Done.' in last_row:
            return self.COMPLETED

        if 'Stopped.' in last_row:
            return self.CANCELED

        if 'Aborting.' in last_row:
            return self.FAILED

        return self.FAILED


def prepare_fields(sender, instance, **kwargs):
    instance.prepare_data()

signals.pre_save.connect(prepare_fields, sender=Project)
signals.pre_save.connect(prepare_fields, sender=ProjectParam)
signals.pre_save.connect(prepare_fields, sender=Stage)
signals.pre_save.connect(prepare_fields, sender=StageParam)
signals.pre_save.connect(prepare_fields, sender=Deploy)
