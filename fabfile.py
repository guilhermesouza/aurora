from fabric.api import local


def setup():
    """Recipe for setup aurora on a local machine"""
    commands = [
        'pip install -r requirements.txt',
        'python -c "from aurora_app.database import init; init()"',
    ]
    map(local, commands)
