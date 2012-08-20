from django import template
from aurora.cruiser.models import ProjectParam, StageParam

register = template.Library()


def show_project_settings(project):
    params = ProjectParam.objects.filter(project=project).order_by('name',)
    repo = project.repository
    return {'params': params, 'repo': repo}


def show_stage_settings(stage):
    params = StageParam.objects.filter(stage=stage).order_by('name',)
    hosts = stage.hosts
    branch = stage.branch
    return {'params': params, 'host': hosts, 'branch': branch}

register.inclusion_tag('settings.html')(show_project_settings)
register.inclusion_tag('settings.html')(show_stage_settings)
