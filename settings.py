import os
import getpass

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'aurora-app'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'aurora.db')
AURORA_PATH = '/home/{}/.aurora/'.format(getpass.getuser())
AURORA_PROJECTS_PATH = os.path.join(AURORA_PATH, 'projects')
AURORA_TMP_PATH = '/tmp/aurora'
AURORA_TMP_DEPLOYMENTS_PATH = os.path.join(AURORA_TMP_PATH, 'deployments')

# Debug toolbar settings
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Celery settings
BROKER_URL = 'sqla+' + SQLALCHEMY_DATABASE_URI

del os
