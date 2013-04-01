import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'aurora-app'
DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'aurora.db')

del os
