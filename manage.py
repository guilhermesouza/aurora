from flask.ext.script import Manager, Server
from flask.ext.alembic import ManageMigrations

from aurora_app import app
from aurora_app.database import db

manager = Manager(app)
manager.add_command("runserver", Server(host=app.config.get('HOST',
                                                            '127.0.0.1'),
                                        port=app.config.get('PORT', 5000)))
manager.add_command("migrate", ManageMigrations())


@manager.command
def setup_submodules():
    """Clones git submodules"""
    import os

    os.system('git submodule init')
    os.system('git submodule update')


@manager.command
def init_db():
    """Creates aurora database."""
    from aurora_app.constants import ROLES
    from aurora_app.models import User

    db.create_all()

    admin = User(username='admin', password='admin', role=ROLES['ADMIN'])
    db.session.add(admin)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
