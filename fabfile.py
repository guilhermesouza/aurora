from fabric.api import local


def init_develop_db():
    """Recipe for creating aurora development database."""
    commands = [
        'python -c "from aurora_app.database import development_init;' +
        'development_init()"',
    ]
    map(local, commands)
