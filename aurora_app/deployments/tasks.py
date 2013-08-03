import os
import imp
import sys
from datetime import datetime

from git import Repo
from fabric.api import execute

from ..decorators import notify_result, task

from .models import Deployment
from .constants import STATUSES


@task
@notify_result
def deploy(deployment_id, session):
    """Runs given deployment."""
    deployment = session.query(Deployment).filter_by(id=deployment_id).first()

    result = {
        'session': session,
        'action': 'create_deployment',
        'category': 'error',
        'user_id': deployment.user_id
    }

    # Create deployment dir
    deployment_tmp_path = deployment.get_tmp_path()
    os.makedirs(deployment_tmp_path)

    deployment_project_tmp_path = os.path.join(
        deployment_tmp_path, deployment.stage.project.get_name_for_path())

    # Copy project's repo if exists, else create an empty folder
    if deployment.stage.project.repository_folder_exists():
        os.system('cp -rf {0} {1}'.format(deployment.stage.project.get_path(),
                                          deployment_project_tmp_path))
    else:
        os.makedirs(deployment_project_tmp_path)

    # Change dir
    os.chdir(deployment_project_tmp_path)

    # Checkout to commit if repo exists
    if deployment.stage.project.repository_folder_exists():
        deployment_repo = Repo.init(deployment_project_tmp_path)
        deployment_repo.git.checkout(deployment.commit)

    # Create module
    module = imp.new_module("deployment_{0}".format(deployment.id))

    # Replace stdout and stderr
    log_path = os.path.join(deployment_tmp_path, 'log')

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = sys.stderr = open(log_path, 'w', 0)

    try:
        print 'Deployment has started.'

        exec deployment.code in module.__dict__

        for task in deployment.tasks:
            # Execute task
            execute(eval('module.' + task.get_function_name()))

        print 'Deployment has finished.'
    except Exception as e:
        deployment.status = STATUSES['FAILED']
        print 'Deployment has failed.'
        print 'Error: {0}'.format(e.message)

        result['message'] = """"{0}" deployment has failed.""" \
            .format(deployment.stage)

    finally:
        # Return stdout and stderr
        sys.stdout.close()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        log_file = open(log_path)

        # If status has not changed
        if deployment.status == STATUSES['RUNNING']:
            deployment.status = STATUSES['COMPLETED']

    deployment.log = '\n'.join(log_file.readlines())
    deployment.finished_at = datetime.now()
    session.add(deployment)
    session.commit()

    # If deployment is successfull
    if deployment.status == STATUSES['COMPLETED']:
        result['category'] = 'success'
        result['message'] = """"{0}" has been deployed successfully.""" \
            .format(deployment.stage)

    return result
