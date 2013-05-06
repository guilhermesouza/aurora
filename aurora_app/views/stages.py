from flask import Blueprint, render_template, request, redirect, url_for, flash

from aurora_app.decorators import must_be_able_to
from aurora_app.forms import StageForm
from aurora_app.models import Project, Stage
from aurora_app.database import db

mod = Blueprint('stages', __name__, url_prefix='/stages')


@mod.route('/create', methods=['GET', 'POST'])
@must_be_able_to('create_stage')
def create():
    project_id = request.args.get('project_id', None)
    project = Project.query.filter_by(id=project_id).first()
    form = StageForm(project=project)

    if form.validate_on_submit():
        stage = Stage(name=form.name.data,
                      code=form.code.data,
                      project=form.project.data)
        db.session.add(stage)
        db.session.commit()

        flash(u'Stage "{}" has been created.'.format(stage.name))
        return redirect(url_for('stages.view', stage_id=stage.id))

    return render_template('stages/create.html', form=form,
                           project_id=project_id)


@mod.route('/view/<int:stage_id>')
def view(stage_id):
    stage = Stage.query.filter_by(id=stage_id).first()
    return render_template('stages/view.html', stage=stage)


@mod.route('/edit/<int:stage_id>', methods=['GET', 'POST'])
@must_be_able_to('edit_stage')
def edit(stage_id):
    stage = Stage.query.filter_by(id=stage_id).first()
    form = StageForm(request.form, stage)

    if form.validate_on_submit():
        form.populate_obj(stage)
        db.session.add(stage)
        db.session.commit()

        flash(u'Stage "{}" has been updated.'.format(stage.name))
        return redirect(url_for('stages.view', stage_id=stage.id))

    return render_template('stages/edit.html', stage=stage, form=form)


@mod.route('/delete/<int:stage_id>')
@must_be_able_to('delete_stage')
def delete(stage_id):
    stage = Stage.query.filter_by(id=stage_id).first()

    project_id = stage.project.id
    flash(u'Stage "{}" has been deleted.'.format(stage.name))

    db.session.delete(stage)
    db.session.commit()

    return redirect(url_for('projects.view', project_id=project_id))
