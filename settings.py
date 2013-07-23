import os
import getpass

_basedir = os.path.abspath(os.path.dirname(__file__))

# flask settings
DEBUG = False
CSRF_ENABLED = True
SECRET_KEY = 'aurora-app'

# sqlalchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'aurora.db')

# aurora settings
AURORA_PATH = '/home/{0}/.aurora/'.format(getpass.getuser())
AURORA_PROJECTS_PATH = os.path.join(AURORA_PATH, 'projects')
AURORA_TMP_PATH = '/tmp/aurora'
AURORA_TMP_DEPLOYMENTS_PATH = os.path.join(AURORA_TMP_PATH, 'deployments')

# Debug toolbar settings
DEBUG_TB_INTERCEPT_REDIRECTS = False

try:
    from local_settings import *
except:
    pass

del os
