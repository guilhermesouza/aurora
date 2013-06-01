from flask import g

from aurora_app import app
from aurora_app.database import db
from aurora_app.models import Project, Notification


@app.context_processor
def projects():
    """Returns all projects."""
    return {'projects': Project.query.all()}


@app.context_processor
def notifications():
    """Marks notifications as seen and returns to user."""
    notifications = Notification.query.filter_by(seen=False, user=g.user) \
                                      .order_by('created_at').all()
    # Update notifications
    for notification in notifications:
        notification.seen = True
    db.session.commit()

    return {'notifications': notifications}
