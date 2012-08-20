from django import template

register = template.Library()


def show_action_button(o):
    return {'o': o}

register.inclusion_tag('action_button.html')(show_action_button)
