from datetime import datetime

from ..extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    message = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(32))
    action = db.Column(db.String(32))
    seen = db.Column(db.Boolean(), default=False)
    # Relations
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id'))

    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"<Notification #{0}>".format(self.id)
