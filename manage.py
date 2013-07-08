from fabric.api import local
from flask.ext.script import Manager

from aurora_app import app

manager = Manager(app)


@manager.command
def celeryd():
    """Starts celery."""
    local('celery worker --app=aurora_app.celery -l debug')


@manager.command
def init_db():
    """Creates aurora database."""
    from aurora_app.database import db
    from aurora_app.constants import ROLES
    from aurora_app.models import User

    db.create_all()

    admin = User(username='admin', password='admin', role=ROLES['ADMIN'])
    db.session.add(admin)
    db.session.commit()


@manager.command
def init_develop_db():
    """Creates aurora development database."""
    from aurora_app.database import db
    from aurora_app.constants import ROLES
    from aurora_app.models import User, Project, Stage

    db.create_all()

    admin = User(username='admin', password='admin', role=ROLES['ADMIN'])
    db.session.add(admin)

    user = User(username='user', password='user')
    db.session.add(user)

    project = Project(name='Aurora',
                      repository_path='https://github.com/ak3n/aurora.git')
    db.session.add(project)

    stage = Stage(name='Development', project=project)
    db.session.add(stage)

    db.session.commit()

if __name__ == "__main__":
    manager.run()
