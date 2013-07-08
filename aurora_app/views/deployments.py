import json

from flask import Blueprint, render_template, request, g, redirect, url_for

from aurora_app.database import get_or_404, db
from aurora_app.models import Project, Stage, Task, Deployment
from aurora_app.decorators import must_be_able_to
from aurora_app.tasks import deploy

mod = Blueprint('deployments', __name__, url_prefix='/deployments')

TIMEOUT = 300


@mod.route('/create/stage/<int:id>', methods=['POST', 'GET'])
@must_be_able_to('deploy_stage')
def create(id):
    stage = get_or_404(Stage, id=id)

    if request.method == 'POST':
        tasks_ids = request.form.getlist('selected')
        tasks = [get_or_404(Task, id=int(task_id)) for task_id in tasks_ids]
        branch = request.form.get('branch')
        commit = request.form.get('commit')

        deployment = Deployment(stage=stage, tasks=tasks,
                                branch=branch, user=g.user, commit=commit)
        db.session.add(deployment)
        db.session.commit()

        deploy.delay(deployment.id)
        return redirect(url_for('deployments.view', id=deployment.id))

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

    if query:
        commits = project.get_all_commits(branch,
                                          skip=page_limit * page)
    else:
        commits = project.get_commits(branch, max_count=page_limit,
                                      skip=page_limit * page)

    result = []
    for commit in commits:
        if query and not (query in commit.hexsha or query in commit.message):
            continue
        else:
            result.append({'id': commit.hexsha,
                           'message': commit.message,
                           'title': "{} - {}".format(commit.hexsha[:10],
                                                     commit.message)})

    total = project.get_commits_count(branch)
    if query:
        total = len(result)
        result = result[:page_limit]

    return json.dumps({'total': total,
                       'commits': result})


@mod.route('/view/<int:id>')
def view(id):
    deployment = get_or_404(Deployment, id=id)
    return render_template('deployments/view.html', deployment=deployment)


@mod.route('/code/<int:id>/fabfile.py')
def raw_code(id):
    deployment = get_or_404(Deployment, id=id)
    return deployment.code, 200, {'Content-Type': 'text/plain'}
