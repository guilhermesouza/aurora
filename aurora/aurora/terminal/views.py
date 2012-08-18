from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse
import pexpect
import md5
import datetime
import os

stages = []


@render_to('terminal.html')
def monitor(request, stage):
    """Allow to watch deploying process"""
    return {'request': request, 'stage': stage}


def start(request, stage):
    """Starts deploy"""
    logfile = open('/tmp/output%s.log' % stage, 'w')
    child = pexpect.spawn('fab hello', logfile=logfile)

    delete_stage(stage, stages)

    child_dict = {'stage': child, 'id': stage, 'messages': []}
    stages.append(child_dict)
    safe_expect(child_dict)
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
    safe_expect(child)
    return HttpResponseRedirect("/terminal/monitor/%s" % stage)


@render_to('log-view.html')
def get_log(request, stage):
    """Returning log of deploy"""
    output = open('/tmp/output%s.log' % stage, 'r').readlines()[1:]
    return {'output': output, 'stage': stage}


#TODO REPLACE IT OMG
def safe_expect(child):
    try:
        child['stage'].expect(get_hash())
    except:
        content = open('/tmp/output%s.log' % child['id'], 'r').readlines()
        logfile = open('/tmp/output%s.log' % child['id'], 'w')
        new_content = ""
        for message in child['messages']:
            for line in content:
                new_content += line.replace(message + message, message)
        logfile.write(new_content)
        logfile.close()


def get_hash():
    return md5.new(str(datetime.datetime.now())).hexdigest()


def delete_stage(stage, stages):
    for item in stages:
        if ('id', stage) in item.items():
            stages.remove(item)
    return stages
