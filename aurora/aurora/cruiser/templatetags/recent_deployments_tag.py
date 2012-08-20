from django import template

register = template.Library()


def show_recent_deployments(deps):
    return {'deps': deps}

register.inclusion_tag('recent_deployments.html')(show_recent_deployments)
