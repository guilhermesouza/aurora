from ..extensions import db
from ..tasks.models import Task
from ..deployments.models import Deployment

stages_tasks_table = db.Table('stages_tasks', db.Model.metadata,
                              db.Column('stage_id', db.Integer,
                                        db.ForeignKey('stages.id')),
                              db.Column('task_id', db.Integer,
                                        db.ForeignKey('tasks.id')))


class Stage(db.Model):
    __tablename__ = "stages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    code = db.Column(db.Text(), default='')
    # Relations
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    deployments = db.relationship(Deployment, backref="stage")
    tasks = db.relationship(Task,
                            secondary=stages_tasks_table,
                            backref="stages")

    def __init__(self, *args, **kwargs):
        super(Stage, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"{0} / {1}".format(self.project.name, self.name) if \
            self.project else self.name