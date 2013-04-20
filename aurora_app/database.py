from flask.ext.sqlalchemy import SQLAlchemy

from aurora_app import app
from aurora_app.constants import ROLES

db = SQLAlchemy(app)


def init():
    from models import User
    db.create_all()

    admin = User(username='admin', password='admin', role=ROLES['ADMIN'])
    db.session.add(admin)
    db.session.commit()
