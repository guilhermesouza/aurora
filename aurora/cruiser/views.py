import os
import pexpect
from multiprocessing import Process
import aurora.settings as settings

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import Project, Stage, Task, Deploy, StageTask, StageUser
from forms import UploadFabFileForm
from lib.fabfile_parser import get_source

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

    try:
        os.fork()
        process.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=2)
    except:
        pass


@login_required
@render_to('base.html')
def index(request):
    deployments = Deploy.objects.all().order_by('-started_at',)[:10]
    return {'deps': deployments}


@login_required
@render_to('project.html')
def project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = UploadFabFileForm(request.POST, request.FILES)
        if form.is_valid():
            fabfile = request.FILES['file']
            content = fabfile.readlines()
            import_block, tasks = get_source(content)

            project.import_block = import_block
            project.save()

            stage = Stage(name="Imported", project=project)
            stage.save()
            stage_user = StageUser(user=request.user, stage=stage)
            stage_user.save()

            for task in tasks:
                task_obj = Task(name=task['name'], body=task['body'])
                task_obj.save()
                stage_task = StageTask(task=task_obj, stage=stage)
                stage_task.save()

    else:
        form = UploadFabFileForm()

    stages = project.stages.order_by('name',)
    deployments = Deploy.objects.filter(stage__in=stages).order_by('-started_at',)[:3]
    return {'p': project, 'stages': stages, 'deps': deployments, 'form': form}


def new_project(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:cruiser_project_add'))


def new_task(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:cruiser_task_add'))


def new_stage(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:cruiser_stage_add'))


@login_required
@render_to('stage.html')
def stage(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)

    project = stage.project
    tasks = stage.tasks.all()
    deployments = stage.deploy_set.order_by('-started_at',)[:3]
    busy = check_perm(stage, request.user)
    return {'p': project, 's': stage, 'tasks': tasks, 'deps': deployments, 'busy': busy}


@login_required
@render_to('task.html')
def task(request, task_id):
    task = get_object_or_None(Task, id=task_id)
    if not task:
        return {'error': "Task is not found"}
    else:
        stages = task.stagetask_set.all()
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
    if stage.already_deploying():
        return 'Sorry stage is deploing now. Please wait a bit and try again.'
    if not stage.permitted_for(user):
        return 'You have no rights to exec.'


@login_required
@render_to('terminal.html')
def monitor(request, deploy_id):
    """Allow to watch deploying process"""
    deploy = get_object_or_404(Deploy, id=deploy_id)
    if not deploy.stage.permitted_for(request.user):
        return HttpResponse(status=403)

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
    if not deploy.stage.permitted_for(request.user):
        return HttpResponse(status=403)

    active_deploy = deploys.get(deploy.id)
    if active_deploy and active_deploy.isalive():
        active_deploy.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=0.5)
    elif deploy.running():
        if active_deploy:
            del(deploys[deploy.id])
        status = deploy.get_status_from_log()
        deploy.finish_with_status(status)

    log = deploy.get_log()

    return {'log': log, 'status': deploy.get_status_display()}


@login_required
def cancel(request, deploy_id):
    """Returning log of deploy"""
    deploy = get_object_or_404(Deploy, id=deploy_id)
    if not deploy.stage.permitted_for(request.user):
        return HttpResponse(status=403)

    active_deploy = deploys.get(deploy.id)
    if active_deploy and active_deploy.terminate():
        del(deploys[deploy.id])
        deploy.finish_with_status(Deploy.CANCELED)

    return HttpResponseRedirect(deploy.get_absolute_url())
