from flask.ext.sqlalchemy import SQLAlchemy
from flask import abort

from aurora_app import app
from aurora_app.constants import ROLES

db = SQLAlchemy(app)


def development_init():
    """Creates database for development."""
    from models import User, Project, Stage
    db.create_all()

    admin = User(username='admin', password='admin', role=ROLES['ADMIN'])
    db.session.add(admin)

    user = User(username='user', password='user')
    db.session.add(user)

    project = Project(name='Aurora')
    db.session.add(project)

    stage = Stage(name='Development', project=project)
    db.session.add(stage)

    db.session.commit()


def get_or_404(model, **kwargs):
    """Returns an object found with kwargs else aborts with 404 page."""
    obj = model.query.filter_by(**kwargs).first()
    if obj is None:
        abort(404)
    return obj
