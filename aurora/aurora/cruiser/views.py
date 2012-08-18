from models import Project, ProjectParam, Stage
from annoying.decorators import render_to


@render_to('base.html')
def index(request):
    pass
    return {}
