from models import Project


def sidebar_data(request):
    return {'projects': Project.objects.order_by('name',)}
