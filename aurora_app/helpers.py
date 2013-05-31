from flask import flash

from aurora_app.models import Notification
from aurora_app.database import db


def notify(message, category=None, action=None):
    """Flashes message and saves as notification in database."""
    notification = Notification(message=message, category=category,
                                action=action)
    db.session.add(notification)
    db.session.commit()

    flash(message, category)
