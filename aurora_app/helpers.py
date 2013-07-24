from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from flask import g

from aurora_app import app
from aurora_app.models import Notification
from aurora_app.database import db


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


def create_folder(path):
    """Creates folder if not exists"""
    import os

    if os.path.exists(path):
        if os.path.isdir(path):
            return
        else:
            raise "Can't create folder because of existing file."

    os.system('mkdir -p {0}'.format(path))


def get_session():
    """Creates session for process"""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = scoped_session(sessionmaker(bind=engine,
                                          autoflush=False,
                                          autocommit=False))
    session = Session()
    setattr(session, '_model_changes', dict())
    return session
