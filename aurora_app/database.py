from flask.ext.sqlalchemy import SQLAlchemy
from flask import abort

from aurora_app import app
from aurora_app.constants import ROLES

db = SQLAlchemy(app)


def init():
    from models import User
    db.create_all()

    admin = User(username='admin', password='admin', role=ROLES['ADMIN'])
    db.session.add(admin)

    user = User(username='user', password='user')
    db.session.add(user)

    db.session.commit()


def get_or_404(model, **kwargs):
    obj = model.query.filter_by(**kwargs).first()
    if obj is None:
        abort(404)
    return obj
