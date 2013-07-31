import os

from flask import url_for

from aurora_app import app
from aurora_app.models import Project, Deployment, Task


@app.context_processor
def projects():
    """Returns all projects."""
    return {'projects': Project.query.all()}


@app.context_processor
def recent_deployments():
    def get_recent_deploments(object):
        if object.__tablename__ == 'projects':
            stages_ids = [stage.id for stage in object.stages]
            result = Deployment.query.filter(
                Deployment.stage_id.in_(stages_ids))
        if object.__tablename__ == 'stages':
            result = Deployment.query.filter_by(stage_id=object.id)
        if object.__tablename__ == 'tasks':
            result = Deployment.query.filter(
                Deployment.tasks.any(Task.id.in_([object.id])))
        if object.__tablename__ == 'users':
            result = Deployment.query.filter_by(user_id=object.id)
        return result.order_by('started_at desc').limit(3).all()
    return dict(get_recent_deployments=get_recent_deploments)


# To exclude caching of static
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
