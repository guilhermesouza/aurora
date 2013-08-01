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


def create_superuser_dialog():
    import getpass
    from email.utils import parseaddr

    print "You need to create a superuser!"

    username = raw_input('Username [{0}]: '.format(getpass.getuser()))
    if not username:
        username = getpass.getuser()

    email = None
    while not email:
        email = parseaddr(raw_input('Email: '))[1]

    passwords = lambda: (getpass.getpass(),
                         getpass.getpass('Password (retype): '))

    password, retyped_password = passwords()

    while password == '' or password != retyped_password:
        print 'Passwords do not match or your password is empty!'
        password, retyped_password = passwords()

    return username, email, password


@manager.command
def init_db():
    """Creates aurora database."""
    from aurora_app.constants import ROLES
    from aurora_app.models import User

    db.create_all()

    username, email, password = create_superuser_dialog()

    admin = User(username=username, password=password, email=email,
                 role=ROLES['ADMIN'])
    db.session.add(admin)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
