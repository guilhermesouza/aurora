from flask import Blueprint, render_template, request

from aurora_app.database import get_or_404
from aurora_app.models import Stage, Task

mod = Blueprint('deployments', __name__, url_prefix='/deployments')


@mod.route('/create/stage/<int:id>', methods=['POST', 'GET'])
def create(id):
    stage = get_or_404(Stage, id=id)

    if request.method == 'POST':
        tasks_ids = request.form.getlist('selected')
        tasks = [get_or_404(Task, id=int(task_id)) for task_id in tasks_ids]

    # Prepare repo vars
    branches = stage.project.get_branches()

    if branches:
        branch = branches[0]
        commits = stage.project.get_commits(branch.name)
    else:
        branch = None
        commits = None

    context = {
        'stage': stage,
        'branch': branch,
        'commits': commits
    }
    return render_template('deployments/create.html', **context)
