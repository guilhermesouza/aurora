from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse
import pexpect

stages = []


@render_to('terminal.html')
def monitor(request, stage):
    """Allow to watch deploying process"""
    return {'request': request, 'stage': stage}


def start(request, stage):
    """Starts deploy"""
    logfile = open('/tmp/output%s.log' % stage, 'w')
    child = pexpect.spawn('fab task', logfile=logfile)
    child.setecho(False)

    child_dict = {'stage': child, 'id': stage, 'messages': []}
    stages.append(child_dict)
    child.expect(pexpect.EOF)
    return HttpResponseRedirect("/terminal/monitor/%s" % stage)


def send(request):
    """Sends a message to process"""
    stage = request.POST.get('stage')
    message = request.POST.get('message')

    if not stage or not message:
        return HttpResponse('Forbidden')

    for child in stages:
        if child['id'] == stage:
            child['stage'].sendline(message)
            child['messages'].append(message)
    child['stage'].expect(pexpect.EOF)
    return HttpResponseRedirect("/terminal/monitor/%s" % stage)


@render_to('log-view.html')
def get_log(request, stage):
    """Returning log of deploy"""
    output = open('/tmp/output%s.log' % stage, 'r').readlines()[1:]
    status = False if get_alive_status(stage) is None else get_alive_status(stage)
    return {'output': output, 'stage': stage, 'isactive': status}


def get_alive_status(id):
    for item in stages:
        if id == item['id']:
            return item['stage'].isalive()
