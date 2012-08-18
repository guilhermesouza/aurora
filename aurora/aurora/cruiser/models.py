from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import datetime

#TODO move it to file?
DEFAULT_IMPORT_BLOCK = "import fabric"

class Project(models.Model):
    """Available projects"""
    name = models.CharField(verbose_name = _('name'), max_length = 32)
    description = models.CharField(verbose_name = _('description'), max_length = 128, null = True, blank = True)
    repository = models.CharField(verbose_name = _('repository'), help_text = _('will be available in recipes as env.repository'), max_length = 128, null = True, blank = True)
    import_block = models.TextField(verbose_name = _('import block'), help_text = _('used in fabfile import block'), default = DEFAULT_IMPORT_BLOCK)

    def __unicode__(self):
        return self.name

class ProjectParams(models.Model):
    """Common params for projects environment"""
    project = models.ForeignKey(Project, verbose_name = _('project'))
    name = models.CharField(verbose_name = _('name'), max_length = 16, help_text = _('env.[name] in recipes'))
    value = models.CharField(verbose_name = _('name'), max_length = 128, help_text = _('use " for strings'))

    def __unicode__(self):
        return "%s: %s = %s " % (self.project.name, self.name, self.value)

class Stage(models.Model):
    """Stages for deployment"""
    name = models.CharField(verbose_name = _('name'), max_length = 32)




