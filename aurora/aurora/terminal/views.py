import pexpect
import os
from django.http import HttpResponse
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from aurora.cruiser.models import Deploy

deploys = {}


@render_to('terminal.html')
def monitor(request, deploy_id):
    """Allow to watch deploying process"""
    return {'request': request, 'deploy_id': deploy_id}


def start(request):
    """Starts deploy"""
    deploy_id = request.POST.get('deploy_id')

    if not deploy_id:
        return HttpResponse('Forbidden')

    deploy = get_object_or_None(Deploy, id=deploy_id)
    deploy_path = deploy.fabfile_path()

    os.chdir(deploy_path)
    logfile = open('output.log', 'w')
    process = pexpect.spawn('fab task', logfile=logfile)
    process.setecho(False)

    deploys[deploy_id] = process
    process.expect(pexpect.EOF)
    return HttpResponse("OK")


def send(request):
    """Sends a message to process"""
    deploy_id = request.POST.get('deploy_id')
    message = request.POST.get('message')

    if not deploy_id or not message:
        return HttpResponse('Forbidden')

    process = deploys.get(deploy_id)
    process.sendline(message)
    process.expect(pexpect.EOF)
    return HttpResponse("OK")


@render_to('log-view.html')
def get_log(request, deploy_id):
    """Returning log of deploy"""
    deploy = get_object_or_None(Deploy, id=deploy_id)
    deploy_path = deploy.fabfile_path()

    os.chdir(deploy_path)
    output = open('output.log', 'r').readlines()[1:]
    status = deploys.get(deploy_id).isalive() or False
    return {'output': output, 'isactive': status}
