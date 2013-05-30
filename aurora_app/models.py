from datetime import datetime
from aurora_app.constants import ROLES, PERMISSIONS, STATUSES
from aurora_app.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.SmallInteger, default=ROLES['USER'])

    def __init__(self, username, password, email=None, role=None):
        self.username = username
        self.set_password(password)
        self.email = email
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def can(self, action):
        return action in PERMISSIONS[self.role]

    def __repr__(self):
        return u'<User {}>'.format(self.username)


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128))
    repo_path = db.Column(db.String(128))
    code = db.Column(db.Text())
    # Relations
    stages = db.relationship("Stage", backref="project")

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.name


stages_tasks_table = db.Table('stages_tasks', db.Model.metadata,
                              db.Column('stage_id', db.Integer,
                                        db.ForeignKey('stages.id')),
                              db.Column('task_id', db.Integer,
                                        db.ForeignKey('tasks.id')))


class Stage(db.Model):
    __tablename__ = "stages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    code = db.Column(db.Text())
    # Relations
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    deployments = db.relationship("Deployment", backref="stage")
    tasks = db.relationship("Task",
                            secondary=stages_tasks_table,
                            backref="stages")

    def __init__(self, *args, **kwargs):
        super(Stage, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"{0} / {1}".format(self.project.name, self.name) if \
            self.project else self.name


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    code = db.Column(db.Text(), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.name


deployments_tasks_table = db.Table('deployments_tasks', db.Model.metadata,
                                   db.Column('deployment_id', db.Integer,
                                             db.ForeignKey('deployments.id')),
                                   db.Column('task_id', db.Integer,
                                             db.ForeignKey('tasks.id')))


class Deployment(db.Model):
    __tablename__ = "deployments"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SmallInteger, default=STATUSES['READY'])
    revision = db.Column(db.String(32))
    started_at = db.Column(db.DateTime(), default=datetime.now)
    finished_at = db.Column(db.DateTime())
    code = db.Column(db.Text())
    log = db.Column(db.Text(), default="")
    # Relations
    stage_id = db.Column(db.Integer(),
                         db.ForeignKey('stages.id'), nullable=False)
    tasks = db.relationship("Task",
                            secondary=deployments_tasks_table,
                            backref="deployments")

    def __init__(self, *args, **kwargs):
        super(Deployment, self).__init__(*args, **kwargs)
