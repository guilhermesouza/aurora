from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core import urlresolvers
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
import aurora.settings as settings
from models import Project, Task, StageTask


@render_to('base.html')
def index(request):
    pass
    return {}


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


@login_required
@render_to('stage.html')
def stage(request, stage_id):
    from models import Stage, Deploy
    busy = False
    stage = get_object_or_None(Stage, id=stage_id)
    if not stage:
        return {}
    else:
        project = stage.project
        tasks = stage.tasks.all()
        deployments = Deploy.objects.filter(stage=stage).order_by('-finished_at',)[:3]
        busy = stage.already_deploying()        
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
    from models import Stage, Task, Deploy, StageTask
    from forms import ExecTaskForm
    busy = None
    stage = get_object_or_404(Stage, id=stage_id)
    task = get_object_or_404(Task, id=task_id)
    get_object_or_404(StageTask, stage=stage, task=task)
    if stage.already_deploying():
        busy = 'Sorry stage is deploing now. Please wait a bit and try again.'
    if request.method == 'POST':
        form = ExecTaskForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['branch'] != '':
                branch = form.cleaned_data['branch']
            comment = form.cleaned_data['comment']
            deploy = Deploy(stage=stage, task=task, branch=branch, user=user)
            deploy.save()
            return HttpResponseRedirect('/')
    else:
        form = ExecTaskForm()
    return {'form': form, 'p': stage.project, 's': stage, 't': task, 'busy': busy}
