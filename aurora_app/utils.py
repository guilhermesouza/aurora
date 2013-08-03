import os

from flask import abort, g, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .notifications.models import Notification
from .extensions import db


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception, e:
        raise e


def get_or_404(model, **kwargs):
    """Returns an object found with kwargs else aborts with 404 page."""
    obj = model.query.filter_by(**kwargs).first()
    if obj is None:
        abort(404)
    return obj


def notify(message, category=None, action=None, user_id=None,
           session=db.session):
    """Wrapper for creating notifications in database."""
    if user_id is None:
        try:
            user_id = g.user.id
        except:
            pass

    notification = Notification(message=message, category=category,
                                action=action, user_id=user_id)
    session.add(notification)
    session.commit()


def get_session():
    """Creates session for process"""
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    Session = scoped_session(sessionmaker(bind=engine,
                                          autoflush=False,
                                          autocommit=False))
    session = Session()
    setattr(session, '_model_changes', dict())
    return session


def build_log_result(lines):
    result = []
    for line in lines:
        result.append('data: {\n' +
                      'data: "message": "{0}"\n'.format(
                          line.replace('\"', '\\\"').replace('\n', '')) +
                      'data: }\n')
    return result