from fabric.api import local


def setup():
    """Recipe for setup aurora on local machine"""
    codemirror_github = 'https://raw.github.com/marijnh/CodeMirror/master'
    codemirror_path = 'aurora_app/cruiser/static/codemirror'
    commands = [
        'pip install -r requirements.txt',
        'python manage.py syncdb',
        'python manage.py migrate',
        'touch aurora_app/local_settings.py',
        'echo "DEBUG = True" > aurora_app/local_settings.py',
        # Download codemirror to static folder
        'wget {0}/lib/codemirror.js -P {1}'.format(codemirror_github, codemirror_path),
        'wget {0}/lib/codemirror.css -P {1}'.format(codemirror_github, codemirror_path),
        'wget {0}/mode/python/python.js -P {1}'.format(codemirror_github, codemirror_path),
        # Run
        'python manage.py run_gunicorn'
    ]
    map(local, commands)
