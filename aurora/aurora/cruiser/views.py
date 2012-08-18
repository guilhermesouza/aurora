from models import Project, ProjectParams, Stage
from annoying.decorators import render_to


@render_to('base.html')
def index(request):
    pass
    return {}
