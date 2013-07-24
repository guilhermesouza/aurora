from flask import (Blueprint, Response, render_template, request, g, redirect,
                   url_for)

from aurora_app.database import get_or_404, db
from aurora_app.models import Stage, Task, Deployment
from aurora_app.decorators import must_be_able_to
from aurora_app.tasks import deploy

mod = Blueprint('deployments', __name__, url_prefix='/deployments')


@mod.route('/create/stage/<int:id>', methods=['POST', 'GET'])
@must_be_able_to('deploy_stage')
def create(id):
    stage = get_or_404(Stage, id=id)
    clone_id = request.args.get('clone')

    if request.method == 'POST':
        tasks_ids = request.form.getlist('selected')

        if tasks_ids == []:
            return "You must select tasks for deployment."

        tasks = [get_or_404(Task, id=int(task_id)) for task_id in tasks_ids]
        branch = request.form.get('branch')
        commit = request.form.get('commit')

        if not commit and stage.project.get_repo() is not None:
            commit = stage.project.get_last_commit(branch).hexsha

        deployment = Deployment(stage=stage, tasks=tasks,
                                branch=branch, user=g.user, commit=commit)
        db.session.add(deployment)
        db.session.commit()

        deploy(deployment.id)
        return redirect(url_for('deployments.view', id=deployment.id))

    # Fetch
    stage.project.fetch()

    branches = stage.project.get_branches()
    if clone_id:
        clone_deployment = get_or_404(Deployment, id=clone_id)

        if clone_deployment.stage.id != stage.id:
            return "Clone deployment should have the same stage."

        # Select clone deployment's branch
        branch = None
        if branches:
            for branch_item in branches:
                if branch_item.name == clone_deployment.branch:
                    branch = branch_item
    else:
        clone_deployment = None
        branch = branches[0] if branches else None

    return render_template('deployments/create.html', stage=stage,
                           branch=branch, clone_deployment=clone_deployment)


@mod.route('/view/<int:id>')
def view(id):
    deployment = get_or_404(Deployment, id=id)
    return render_template('deployments/view.html', deployment=deployment)


@mod.route('/code/<int:id>/fabfile.py')
def raw_code(id):
    deployment = get_or_404(Deployment, id=id)
    return Response(deployment.code, mimetype='text/plain')


@mod.route('/log/<int:id>')
def log(id):
    deployment = get_or_404(Deployment, id=id)
    lines = deployment.get_log_lines()
    return render_template('deployments/log.html', lines=lines)
