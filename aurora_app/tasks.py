from __future__ import absolute_import

import os
import imp
import sys
from datetime import datetime

from git import Repo
from fabric.api import local, execute

from aurora_app import celery, app
from aurora_app.database import db
from aurora_app.models import Deployment
from aurora_app.helpers import notify
from aurora_app.constants import STATUSES


@celery.task(ignore_result=True)
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

    if not os.path.exists(project_path):
        notify("""Can't clone "{}" repository. Something gone wrong.""".
               format(project.name),
               category='error', action=action, user_id=user_id)
        return

    notify("""Cloning "{}" repository has finished successfully.""".
           format(project.name, project_path),
           category='success', action=action, user_id=user_id)


@celery.task(ignore_result=True)
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

    if os.path.exists(project_path):
        notify("""Can't remove "{}" repository. Something gone wrong.""".
               format(project.name),
               category='error', action=action, user_id=user_id)
        return

    notify(""""{}" repository has removed successfully.""".
           format(project.name, project_path),
           category='success', action=action, user_id=user_id)


@celery.task(ignore_result=True)
def deploy(deployment_id):
    """Run's given deployment."""
    action = 'deploy_stage'
    deployment = Deployment.query.filter_by(id=deployment_id).first()

    # Copy project to tmp
    deployment_tmp_path = os.path.join(
        app.config['AURORA_TMP_DEPLOYMENTS_PATH'], '{}'.format(deployment.id))
    os.system('cp -rf {} {}'.format(deployment.stage.project.get_path(),
                                    deployment_tmp_path))

    # Change dir
    os.chdir(deployment_tmp_path)

    # Checkout to commit
    deployment_repo = Repo.init(deployment_tmp_path)
    deployment_repo.git.checkout(deployment.commit)

    # Create module
    module = imp.new_module("deployment_{}".format(deployment.id))
    exec deployment.code in module.__dict__
    # Replace stdout
    log_path = os.path.join(deployment_tmp_path, 'deployment.log')
    old_stdout = sys.stdout
    sys.stdout = open(log_path, 'w', 0)

    # Update status
    deployment.status = STATUSES['RUNNING']
    db.session.add(deployment)
    db.session.commit()

    try:
        print 'Deployment has started.'
        for task in deployment.tasks:
            # Execute task
            execute(eval('module.' + task.get_function_name()))
        print 'Deployment has finished.'
    except Exception as e:
        deployment.status = STATUSES['FAILED']
        print 'Deployment has failed.'
        print 'Error: {}'.format(e.message)

        notify(""""{}" deployement has failed."""
               .format(deployment.stage),
               category='error', action=action, user_id=deployment.user_id)

    finally:
        # Return stdout
        sys.stdout.close()
        sys.stdout = old_stdout
        log_file = open(log_path)

        # If status has not changed
        if deployment.status == STATUSES['RUNNING']:
            deployment.status = STATUSES['COMPLETED']

    deployment.log = '\n'.join(log_file.readlines())
    deployment.finished_at = datetime.now()
    db.session.add(deployment)
    db.session.commit()

    notify(""""{}" has been deployed successfully."""
           .format(deployment.stage),
           category='success', action=action, user_id=deployment.user_id)
