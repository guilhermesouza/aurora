from flask.ext.sqlalchemy import SQLAlchemy
from flask import abort

from aurora_app import app

db = SQLAlchemy(app)


def get_or_404(model, **kwargs):
    """Returns an object found with kwargs else aborts with 404 page."""
    obj = model.query.filter_by(**kwargs).first()
    if obj is None:
        abort(404)
    return obj
