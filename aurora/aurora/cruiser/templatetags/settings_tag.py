from django import template
from aurora.cruiser.models import ProjectParam, StageParam

register = template.Library()


def show_project_settings(project):
#    params = ProjectParam.objects.filter(project=project).order_by('name',)
    print project.params()
    return {'params': project.params()}


def show_stage_settings(stage):
    params = StageParam.objects.filter(stage=stage).order_by('name',)
    return {'params': params}

register.inclusion_tag('settings.html')(show_project_settings)
register.inclusion_tag('settings.html')(show_stage_settings)
