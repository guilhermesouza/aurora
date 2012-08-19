import os
import sys

sys.path = ['/web/aurora.local', '/web/aurora.local/releases/current/aurora.local/aurora', '/web/aurora.local/lib/python2.6/site-packages'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'aurora.settings'
os.environ['PYTHON_EGG_CACHE'] = '/web/aurora.local/.python-eggs'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
