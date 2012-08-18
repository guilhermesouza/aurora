from models import Project, Task
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
import aurora.settings as settings
from django.http import HttpResponseRedirect
from django.core import urlresolvers


@render_to('base.html')
def index(request):
    pass
    return {}


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


@render_to('stage.html')
def stage(request, stage_id):
    from models import Stage, Deploy
    stage = get_object_or_None(Stage, id=stage_id)
    if not stage:
        return {}
    else:
        project = stage.project
        tasks = stage.tasks.all()
        deployments = Deploy.objects.filter(stage=stage).order_by('-finished_at',)[:3]
        return {'p': project, 's': stage, 'tasks': tasks, 'deps': deployments}


@render_to('task.html')
def task(request, task_id):
    task = get_object_or_None(Task, id=task_id)
    if not task:
        return {}
    else:
        return {'task': task}


@render_to('500.html')
def server_error(request):
    return {'STATIC_URL': settings.STATIC_URL}


@render_to('exec.html')
def exec_task(request, stage_id, task_id):
    from models import Stage, Task
    from forms import ExecForm
    stage = get_object_or_None(Stage, id=stage_id)
    task = get_object_or_None(Task, id=task_id)
    if stage and task:
        try:
            task = stage.tasks.filter(task=task)
        except:
            pass
        if request.method == 'POST':
            form = ExecForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['branch'] != '':
                    return HttpResponseNotFound('<h1>Fuck you, robot.</h1>')
                email = form.cleaned_data['email']
                создать деплой
                return {}
            else:
                form = ExecForm()
            return {'form': form}
    else:
        return {}
