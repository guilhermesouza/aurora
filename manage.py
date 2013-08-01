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

    submodules_tags = {
        'bootstrap': 'v3.0.0-rc1',
        'bootbox': 'v3.3.0',
        'select2': '3.4.1'
    }

    submodules_path_prefix = 'aurora_app/static/'

    for submodule_name, tag in submodules_tags.iteritems():
        os.system('cd {0}; git checkout {1}'.format(
            os.path.join(submodules_path_prefix, submodule_name), tag))


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
