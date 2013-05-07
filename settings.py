import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'aurora-app'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'aurora.db')

# Debug toolbar settings
DEBUG_TB_INTERCEPT_REDIRECTS = False

del os
