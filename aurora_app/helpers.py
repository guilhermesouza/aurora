from flask import g

from aurora_app.models import Notification
from aurora_app.database import db


def notify(message, category=None, action=None, user_id=None):
    """Wrapper for creating notifications in database."""
    if user_id is None:
        try:
            user_id = g.user.id
        except:
            pass

    notification = Notification(message=message, category=category,
                                action=action, user_id=user_id)
    db.session.add(notification)
    db.session.commit()


def create_folder(path):
    """Creates folder if not exists"""
    import os

    if os.path.exists(path):
        if os.path.isdir(path):
            return
        else:
            raise "Can't create folder because of existing file."

    os.system('mkdir -p {}'.format(path))
