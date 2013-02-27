from fabric.api import local


def local_setup():
    """Recipe for setup aurora on local machine"""
    commands = [
        'pip install -r requirements.txt',
        'python manage.py syncdb',
        'python manage.py migrate',
        'touch aurora/local_settings.py',
        'echo "DEBUG = True" > aurora/local_settings.py'
    ]
    map(local, commands)
