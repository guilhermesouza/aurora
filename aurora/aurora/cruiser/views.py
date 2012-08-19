import os
import pexpect
import aurora.settings as settings

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import Project, Stage, Task, Deploy, StageTask

deploys = {}


def run_deploy(deploy):
    """Run deploy"""
    if deploys.get(deploy.id) or not deploy.run():
        return False

    deploy.build_fabfile()
    os.chdir(deploy.working_path())
    logfile = open('output.log', 'w')
    command = 'fab %s' % deploy.task.name
    process = pexpect.spawn(command, logfile=logfile)
    process.setecho(False)

    deploys[deploy.id] = process


@login_required
@render_to('base.html')
def index(request):
    from models import Deploy
    deployments = Deploy.objects.all().order_by('-finished_at',)[:10]
    return {'deps': deployments}


@login_required
@render_to('project.html')
def project(request, project_id):
    from models import Stage, Deploy
    project = get_object_or_None(Project, id=project_id)
    if not project:
        return {}
    else:
        stages = Stage.objects.filter(project=project).order_by('name',)
        deployments = Deploy.objects.filter(stage__in=stages).order_by('-finished_at',)[:3]
        return {'p': project, 'stages': stages, 'deps': deployments}


def new_project(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:cruiser_project_add'))


def new_task(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:cruiser_task_add'))


def new_stage(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:cruiser_stage_add'))


@login_required
@render_to('stage.html')
def stage(request, stage_id):
    from models import Stage, Deploy
    busy = None
    stage = get_object_or_None(Stage, id=stage_id)
    if not stage:
        return {}
    else:
        project = stage.project
        tasks = stage.tasks.all()
        deployments = Deploy.objects.filter(stage=stage).order_by('-finished_at',)[:3]
        busy = check_perm(stage, request.user)
        return {'p': project, 's': stage, 'tasks': tasks, 'deps': deployments, 'busy': busy}


@login_required
@render_to('task.html')
def task(request, task_id):
    task = get_object_or_None(Task, id=task_id)
    if not task:
        return {'error': "Task is not found"}
    else:
        stages = StageTask.objects.filter(task=task)
        return {'task': task, 'stages': stages}


@render_to('500.html')
def server_error(request):
    return {'STATIC_URL': settings.STATIC_URL}


@login_required
@render_to('exec.html')
def exec_task(request, stage_id, task_id):
    from forms import ExecTaskForm

    stage = get_object_or_404(Stage, id=stage_id)
    task = get_object_or_404(Task, id=task_id)
    get_object_or_404(StageTask, stage=stage, task=task)
    busy = check_perm(stage, request.user)

    form = ExecTaskForm(request.POST or None)
    if form.is_valid():
        branch = form.cleaned_data['branch']
        comment = form.cleaned_data['comment']
        deploy = Deploy(stage=stage, task=task, branch=branch, user=request.user, comment=comment)
        deploy.save()

        run_deploy(deploy)
        return HttpResponseRedirect(deploy.get_absolute_url())

    return {'form': form, 'p': stage.project, 's': stage, 't': task, 'busy': busy}


def check_perm(stage, user):
    from models import StageUser
    if stage.already_deploying():
        return 'Sorry stage is deploing now. Please wait a bit and try again.'
    if not get_object_or_None(StageUser, stage=stage, user=user):
        return 'You have no rights to exec.'


@login_required
@render_to('terminal.html')
def monitor(request, deploy_id):
    """Allow to watch deploying process"""
    deploy = get_object_or_404(Deploy, id=deploy_id)

    return {'deploy': deploy}


@login_required
def send(request, deploy_id):
    """Sends a message to process"""
    message = request.POST.get('message')

    if not message:
        return HttpResponse('Forbidden')

    process = deploys.get(int(deploy_id))
    if process:
        process.sendline(message)

    return HttpResponse("OK")


@login_required
@render_to('log-view.html')
def get_log(request, deploy_id):
    """Returning log of deploy"""
    deploy = get_object_or_404(Deploy, id=deploy_id)

    active_deploy = deploys.get(deploy.id)
    if active_deploy:
        active_deploy.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=1)
        if not active_deploy.isalive():
            deploy.finish_with_status(Deploy.COMPLETED)

    log = deploy.get_log()

    return {'log': log, 'status': deploy.get_status_display()}
