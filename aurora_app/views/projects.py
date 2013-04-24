from flask import Blueprint, render_template, url_for, redirect, flash

from aurora_app.constants import ROLES
from aurora_app.decorators import need_to_be
from aurora_app.forms import ProjectForm
from aurora_app.models import Project
from aurora_app.database import db

mod = Blueprint('projects', __name__, url_prefix='/projects')


@mod.route('/create', methods=['GET', 'POST'])
@need_to_be(role=ROLES['ADMIN'])
def create():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          repo_path=form.repo_path.data)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects.view', project_id=project.id))
    return render_template('projects/create.html', form=form)


@mod.route('/view/<int:project_id>')
def view(project_id):
    project = Project.query.filter_by(id=project_id).first()
    return render_template('projects/view.html', project=project)


@mod.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit(project_id):
    project = Project.query.filter_by(id=project_id).first()
    form = ProjectForm(**project.__dict__)

    if form.validate_on_submit():
        [setattr(project, attr, value) for attr, value in form.data.items()]
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects.view', project_id=project_id))

    return render_template('projects/edit.html', project=project, form=form)


@mod.route('/delete/<int:project_id>')
def delete(project_id):
    project = Project.query.filter_by(id=project_id).first()
    flash(u'Project "{}" has been deleted.'.format(project.name))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('main.index'))
