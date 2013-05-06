from flask import Blueprint, render_template, url_for, redirect, flash, request

from aurora_app.decorators import must_be_able_to
from aurora_app.forms import ProjectForm
from aurora_app.models import Project
from aurora_app.database import db

mod = Blueprint('projects', __name__, url_prefix='/projects')


@mod.route('/create', methods=['GET', 'POST'])
@must_be_able_to('create_project')
def create():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          repo_path=form.repo_path.data)
        db.session.add(project)
        db.session.commit()

        flash(u'Project "{}" has been created.'.format(project.name))
        return redirect(url_for('projects.view', project_id=project.id))

    return render_template('projects/create.html', form=form)


@mod.route('/view/<int:project_id>')
def view(project_id):
    project = Project.query.filter_by(id=project_id).first()
    return render_template('projects/view.html', project=project)


@mod.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@must_be_able_to('edit_project')
def edit(project_id):
    project = Project.query.filter_by(id=project_id).first()
    form = ProjectForm(request.form, project)

    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.add(project)
        db.session.commit()

        flash(u'Project "{}" has been updated.'.format(project.name))
        return redirect(url_for('projects.view', project_id=project_id))

    return render_template('projects/edit.html', project=project, form=form)


@mod.route('/delete/<int:project_id>')
@must_be_able_to('delete_project')
def delete(project_id):
    project = Project.query.filter_by(id=project_id).first()

    flash(u'Project "{}" has been deleted.'.format(project.name))

    # Delete stages
    for stage in project.stages:
        db.session.delete(stage)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('main.index'))
