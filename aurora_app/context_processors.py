import os

from flask import url_for

from aurora_app import app
from aurora_app.models import Project


@app.context_processor
def projects():
    """Returns all projects."""
    return {'projects': Project.query.all()}


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
