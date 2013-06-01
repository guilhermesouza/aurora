from __future__ import absolute_import
import os

from celery import Task

from fabric.api import local

from aurora_app import app, celery
from aurora_app.helpers import notify


class TaskWithNotification(Task):
    abstract = True

    def on_failure(self, *args, **kwargs):
        exc = kwargs.get('exc')
        message = exc.message if exc is not None else 'No message.'
        notify("Task {} failed: {}".format(self.request, message),
               category='error')


@celery.task(base=TaskWithNotification, ignore_result=True)
def clone_git_project(project, user_id=None):
    """Clones project's git repository to Aurora folder."""
    if project.repo_path == '':
        notify("""Can't clone "{}" git repository without path.""".
               format(project.name),
               category='error', action='clone_git_project', user_id=user_id)
        return

    full_repo_path = os.path.join(app.config['AURORA_PATH'],
                                  project.get_path_name())
    if os.path.exists(full_repo_path):
        notify("""Can't clone "{}" git repository. "{}" is exists.""".
               format(project.name, full_repo_path),
               category='error', action='clone_git_project', user_id=user_id)
        return

    local('git clone {} {}'.format(project.repo_path, full_repo_path))
    notify("""Cloning "{}" git repository has finished successfully.""".
           format(project.name, full_repo_path),
           category='success', action='clone_git_project', user_id=user_id)
