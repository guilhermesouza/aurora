import json

from flask import Blueprint, render_template, request

from aurora_app.database import get_or_404
from aurora_app.models import Project, Stage, Task
from aurora_app.decorators import must_be_able_to

mod = Blueprint('deployments', __name__, url_prefix='/deployments')


@mod.route('/create/stage/<int:id>', methods=['POST', 'GET'])
@must_be_able_to('deploy_stage')
def create(id):
    stage = get_or_404(Stage, id=id)

    if request.method == 'POST':
        tasks_ids = request.form.getlist('selected')
        tasks = [get_or_404(Task, id=int(task_id)) for task_id in tasks_ids]

    # Prepare repo vars
    branches = stage.project.get_branches()

    branch = branches[0] if branches else None
    return render_template('deployments/create.html',
                           stage=stage, branch=branch)


@mod.route('/commits/<int:id>')
def commits(id):
    project = get_or_404(Project, id=id)
    branch = request.args.get('branch')
    query = request.args.get('query')
    page_limit = int(request.args.get('page_limit'))
    page = int(request.args.get('page'))
    commits = project.get_commits(branch, max_count=page_limit,
                                  skip=page_limit * page)
    result = []

    for commit in commits:
        if query in commit.hexsha or query in commit.message:
            result.append({'id': commit.hexsha,
                           'message': commit.message,
                           'title': "{} - {}".format(commit.hexsha[:10],
                                                     commit.message)})
    return json.dumps({'total': project.get_commits_count(branch),
                       'commits': result})
