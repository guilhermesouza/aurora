from flask import Blueprint, render_template, g, Response

from aurora_app.database import db
from aurora_app.models import Notification

mod = Blueprint('notifications', __name__, url_prefix='/notifications')


@mod.route('/table')
def table():
    notifications = Notification.query.order_by("created_at desc").all()
    return render_template('notifications/table.html',
                           notifications=notifications)


@mod.route('/unseen')
def unseen():
    """Returns unseen notifications and updates them as seen."""
    notifications = Notification.query.filter_by(seen=False, user=g.user) \
                                      .order_by('created_at').all()

    notifications_for_response = []
    # Update notifications
    for notification in notifications:
        notification.seen = True
        notifications_for_response.append({'message': notification.message,
                                           'category': notification.category})
    db.session.commit()

    def generate():
        for notification in notifications_for_response:
            result = "data: {\n"
            result += 'data: "message": "{0}",\n'.format(
                notification['message'].replace('\"', '\\\"'))
            result += 'data: "category": "{0}"\n'.format(
                notification['category'])
            result += "data: }\n\n"
            yield result

    return Response(generate(), mimetype='text/event-stream')
