from flask import Blueprint, render_template, request, redirect, url_for, flash

from aurora_app.decorators import must_be_able_to
from aurora_app.forms import StageForm
from aurora_app.models import Project, Stage
from aurora_app.database import db, get_or_404

mod = Blueprint('stages', __name__, url_prefix='/stages')


@mod.route('/create', methods=['GET', 'POST'])
@must_be_able_to('create_stage')
def create():
    project_id = request.args.get('project_id', None)
    project = get_or_404(Project, id=project_id) if project_id else None
    form = StageForm(project=project)

    if form.validate_on_submit():
        stage = Stage()
        form.populate_obj(stage)
        db.session.add(stage)
        db.session.commit()

        flash(u'Stage "{}" has been created.'.format(stage.name))
        return redirect(url_for('stages.view', id=stage.id))

    return render_template('stages/create.html', form=form, id=project_id)


@mod.route('/view/<int:id>')
def view(id):
    stage = get_or_404(Stage, id=id)
    return render_template('stages/view.html', stage=stage)


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@must_be_able_to('edit_stage')
def edit(id):
    stage = get_or_404(Stage, id=id)
    form = StageForm(request.form, stage)

    if form.validate_on_submit():
        form.populate_obj(stage)
        db.session.add(stage)
        db.session.commit()

        flash(u'Stage "{}" has been updated.'.format(stage.name))
        return redirect(url_for('stages.view', id=stage.id))

    return render_template('stages/edit.html', stage=stage, form=form)


@mod.route('/delete/<int:id>')
@must_be_able_to('delete_stage')
def delete(id):
    stage = get_or_404(Stage, id=id)

    project_id = stage.project.id
    flash(u'Stage "{}" has been deleted.'.format(stage.name))

    db.session.delete(stage)
    db.session.commit()

    return redirect(url_for('projects.view', id=project_id))


@mod.route('/table')
def table():
    stages = Stage.query.all()
    return render_template('stages/table.html', stages=stages)
