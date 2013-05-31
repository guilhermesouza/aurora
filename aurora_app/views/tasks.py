from flask import Blueprint, render_template, request, redirect, url_for

from aurora_app.decorators import must_be_able_to
from aurora_app.forms import TaskForm
from aurora_app.models import Stage, Task
from aurora_app.database import db, get_or_404
from aurora_app.helpers import notify

mod = Blueprint('tasks', __name__, url_prefix='/tasks')


@mod.route('/create', methods=['GET', 'POST'])
@must_be_able_to('create_task')
def create():
    stage_id = request.args.get('stage_id', None)
    stage = get_or_404(Stage, id=stage_id) if stage_id else None
    form = TaskForm(stages=[stage])

    if form.validate_on_submit():
        task = Task()
        form.populate_obj(task)
        db.session.add(task)
        db.session.commit()

        notify(u'Task "{}" has been created.'.format(task.name),
               category='success', action='create_task')
        return redirect(url_for('tasks.view', id=task.id))

    return render_template('tasks/create.html', form=form, stage_id=stage_id)


@mod.route('/view/<int:id>')
def view(id):
    task = get_or_404(Task, id=id)
    return render_template('tasks/view.html', task=task)


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@must_be_able_to('edit_task')
def edit(id):
    task = get_or_404(Task, id=id)
    form = TaskForm(request.form, task)

    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.add(task)
        db.session.commit()

        notify(u'Task "{}" has been updated.'.format(task.name),
               category='success', action='edit_task')
        return redirect(url_for('tasks.view', id=task.id))

    return render_template('tasks/edit.html', task=task, form=form)


@mod.route('/delete/<int:id>')
@must_be_able_to('delete_task')
def delete(id):
    task = get_or_404(Task, id=id)

    notify(u'Task "{}" has been deleted.'.format(task.name),
           category='success', action='delete_task')

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('main.index'))


@mod.route('/table')
def table():
    tasks = Task.query.all()
    return render_template('tasks/table.html', tasks=tasks)
