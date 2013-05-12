from flask import Blueprint, render_template, url_for, redirect, flash, request

from aurora_app.decorators import must_be_able_to
from aurora_app.forms import ProjectForm
from aurora_app.models import Project
from aurora_app.database import db, get_or_404

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

        flash(u'Project "{}" has been created.'.format(project.name), 'success')
        return redirect(url_for('projects.view', id=project.id))

    return render_template('projects/create.html', form=form)


@mod.route('/view/<int:id>')
def view(id):
    project = get_or_404(Project, id=id)
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

        flash(u'Project "{}" has been updated.'.format(project.name), 'success')
        return redirect(url_for('projects.view', id=id))

    return render_template('projects/edit.html', project=project, form=form)


@mod.route('/delete/<int:id>')
@must_be_able_to('delete_project')
def delete(id):
    project = get_or_404(Project, id=id)

    flash(u'Project "{}" has been deleted.'.format(project.name), 'success')

    # Delete stages
    for stage in project.stages:
        db.session.delete(stage)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('main.index'))
