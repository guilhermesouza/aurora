from models import Project, Task, Stage


def sidebar_data(request):
    return {'all_projects': Project.objects.order_by('name',),
            'all_tasks': Task.objects.order_by('name',),
            'all_stages': Stage.objects.order_by('name',)}
