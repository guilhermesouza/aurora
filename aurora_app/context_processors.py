from aurora_app import app
from aurora_app.models import Project


@app.context_processor
def projects():
    """Returns all projects."""
    return {'projects': Project.query.all()}
