import os
import sys

sys.path = ['/web/aurora.fefelovgroup.com', '/web/aurora.fefelovgroup.com/releases/current/aurora.fefelovgroup.com/aurora', '/web/aurora.fefelovgroup.com/lib/python2.6/site-packages'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'aurora.settings'
os.environ['PYTHON_EGG_CACHE'] = '/web/aurora.fefelovgroup.com/.python-eggs'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
