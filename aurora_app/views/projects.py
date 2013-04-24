from flask import Blueprint, render_template, url_for, redirect

from aurora_app.constants import ROLES
from aurora_app.decorators import need_to_be
from aurora_app.forms import CreateProjectForm
from aurora_app.models import Project
from aurora_app.database import db

mod = Blueprint('projects', __name__, url_prefix='/projects')


@mod.route('/create', methods=['GET', 'POST'])
@need_to_be(role=ROLES['ADMIN'])
def create():
    form = CreateProjectForm()

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
