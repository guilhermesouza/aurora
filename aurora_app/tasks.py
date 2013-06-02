from __future__ import absolute_import
import os

from celery import Task

from fabric.api import local

from aurora_app import celery
from aurora_app.helpers import notify


class TaskWithNotification(Task):
    abstract = True

    def on_failure(self, *args, **kwargs):
        exc = kwargs.get('exc')
        message = exc.message if exc is not None else 'No message.'
        notify("Task {} failed: {}".format(self.request, message),
               category='error')


@celery.task(base=TaskWithNotification, ignore_result=True)
def clone_repository(project, user_id=None):
    """Clones project's repository to Aurora folder."""
    action = 'clone_repository'
    if project.repository_path == '':
        notify("""Can't clone "{}" repository without path.""".
               format(project.name),
               category='error', action=action, user_id=user_id)
        return

    project_path = project.get_path()
    if os.path.exists(project_path):
        notify("""Can't clone "{}" repository. "{}" is exists.""".
               format(project.name, project_path),
               category='error', action=action, user_id=user_id)
        return

    local('git clone {} {}'.format(project.repository_path, project_path))
    notify("""Cloning "{}" repository has finished successfully.""".
           format(project.name, project_path),
           category='success', action=action, user_id=user_id)


@celery.task(base=TaskWithNotification, ignore_result=True)
def remove_repository(project, user_id=None):
    """Removes project's repository in Aurora folder."""
    action = 'remove_repository'
    project_path = project.get_path()
    if not os.path.exists(project_path):
        notify("""Can't remove "{}" repository. It's not exists.""".
               format(project.name),
               category='error', action=action, user_id=user_id)
        return

    local('rm -rf {}'.format(project_path))
    notify(""""{}" repository has removed successfully.""".
           format(project.name, project_path),
           category='success', action=action, user_id=user_id)
