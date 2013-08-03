from flask import Blueprint, render_template, g, Response

from ..extensions import db

from .models import Notification

notifications = Blueprint('notifications', __name__,
                          url_prefix='/notifications')


@notifications.route('/')
def all():
    notifications = Notification.query.order_by("created_at desc").all()
    return render_template('notifications/all.html',
                           notifications=notifications)


@notifications.route('/unseen')
def unseen():
    """Returns unseen notifications and updates them as seen."""
    notifications = Notification.query.filter_by(seen=False, user=g.user) \
                                      .order_by('created_at').all()

    notifications_for_response = []
    # Update notifications
    for notification in notifications:
        notification.seen = True
        category = 'danger' if notification.category == 'error' else \
            notification.category
        notifications_for_response.append({'message': notification.message,
                                           'category': category})
    db.session.commit()

    def generate():
        for notification in notifications_for_response:
            result = 'data: {\n' + \
                     'data: "message": "{0}",\n'.format(
                         notification['message'].replace('\"', '\\\"')) +\
                     'data: "category": "{0}"\n'.format(
                         notification['category']) +\
                     'data: }\n\n'
            yield result

    return Response(generate(), mimetype='text/event-stream')
