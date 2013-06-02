from flask import (Blueprint, render_template, url_for, redirect, request, g,
                   json)

from aurora_app.decorators import must_be_able_to
from aurora_app.forms import ProjectForm
from aurora_app.models import Project
from aurora_app.database import db, get_or_404
from aurora_app.helpers import notify
from aurora_app.tasks import clone_repository, remove_repository

mod = Blueprint('projects', __name__, url_prefix='/projects')


@mod.route('/create', methods=['GET', 'POST'])
@must_be_able_to('create_project')
def create():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project()
        form.populate_obj(project)
        db.session.add(project)
        db.session.commit()

        notify(u'Project "{}" has been created.'.format(project.name),
               category='success', action='create_project')
        return redirect(url_for('projects.view', id=project.id))

    return render_template('projects/create.html', form=form)


@mod.route('/view/<int:id>')
def view(id):
    project = get_or_404(Project, id=id)
    # clone_git_project.delay(project, g.user.id)
    return render_template('projects/view.html', project=project)


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@must_be_able_to('edit_project')
def edit(id):
    project = get_or_404(Project, id=id)
    form = ProjectForm(request.form, project)

    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.add(project)
        db.session.commit()

        notify(u'Project "{}" has been updated.'.format(project.name),
               category='success', action='edit_project')
        return redirect(url_for('projects.view', id=id))

    return render_template('projects/edit.html', project=project, form=form)


@mod.route('/delete/<int:id>')
@must_be_able_to('delete_project')
def delete(id):
    project = get_or_404(Project, id=id)

    notify(u'Project "{}" has been deleted.'.format(project.name),
           category='success', action='delete_project')

    # Delete stages
    for stage in project.stages:
        db.session.delete(stage)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('main.index'))


TASKS = {
    'clone_repository': clone_repository,
    'remove_repository': remove_repository
}


@mod.route('/execute/<int:id>', methods=['POST'])
def execute(id):
    project = get_or_404(Project, id=id)
    action = request.form.get('action')
    if g.user.can(action):
        TASKS[action](project)
        return json.dumps({'error': False})

    notify(u"""Can't execute "{}.{}".""".format(project.name, action),
           category='error', action=action, user_id=g.user.id)
    return json.dumps({'error': True})
