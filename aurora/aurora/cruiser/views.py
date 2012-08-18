from models import Project, ProjectParam, Stage
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
import aurora.settings as settings


@render_to('base.html')
def index(request):
    pass
    return {}


@render_to('project.html')
def project(request, project_id):
    project = get_object_or_None(Project, id=project_id)
    if not project:
        return {}
    else:
        return {'project': project}


@render_to('500.html')
def server_error(request):
    return {'STATIC_URL': settings.STATIC_URL}
