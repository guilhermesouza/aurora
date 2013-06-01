from aurora_app.models import Notification
from aurora_app.database import db


def notify(message, category=None, action=None, user_id=None):
    """Wrapper for creating notifications in database."""
    notification = Notification(message=message, category=category,
                                action=action, user_id=user_id)
    db.session.add(notification)
    db.session.commit()


def create_aurora_folder(path):
    """Creates Aurora folder if not exists"""
    import os

    if os.path.exists(path):
        if os.path.isdir(path):
            return
        else:
            raise "Can't create Aurora folder because of existing file."

    os.system('mkdir -p {}'.format(path))
