from fabric.api import local


def local_setup():
    """Recipe for setup aurora on local machine"""
    commands = [
        'pip install -r requirements.txt',
        'python manage.py syncdb',
        'python manage.py migrate',
        'touch aurora/local_settings.py',
        'echo "DEBUG = True" > aurora/local_settings.py',
        # Download codemirror to static folder
        'wget https://raw.github.com/marijnh/CodeMirror/master/lib/codemirror.js -P static/codemirror',
        'wget https://raw.github.com/marijnh/CodeMirror/master/lib/codemirror.css -P static/codemirror',
        'wget https://raw.github.com/marijnh/CodeMirror/master/mode/python/python.js -P static/codemirror'
    ]
    map(local, commands)
