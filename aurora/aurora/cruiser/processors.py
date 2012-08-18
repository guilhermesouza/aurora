from models import Project, Task


def sidebar_data(request):
    return {'projects': Project.objects.order_by('name',),
            'tasks': Task.objects.order_by('name',)}
