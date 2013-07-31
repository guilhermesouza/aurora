from flask import Blueprint, render_template, redirect, url_for, request

from aurora_app.decorators import must_be_able_to
from aurora_app.models import User
from aurora_app.database import db, get_or_404
from aurora_app.helpers import notify
from aurora_app.forms import EditUserForm, CreateUserForm

mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/create', methods=['GET', 'POST'])
@must_be_able_to('create_user')
def create():
    form = CreateUserForm()

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)

        # Check for duplicates
        if User.query.filter_by(username=form.username.data).first() is None:
            db.session.add(user)
            db.session.commit()

            notify(u'User "{0}" has been created.'.format(user.username),
                   category='success', action='create_user')
            return redirect(url_for('users.view', id=user.id))
        form.username.errors = [u'Choose another username, please.']

    return render_template('users/create.html', form=form)

@mod.route('/view/<int:id>')
def view(id):
    user = get_or_404(User, id=id)
    return render_template('users/view.html', user=user)


@mod.route('/')
def all():
    users = User.query.all()
    return render_template('users/all.html', users=users)


@mod.route('/delete/<int:id>')
@must_be_able_to('delete_user')
def delete(id):
    user = get_or_404(User, id=id)

    notify(u'User "{0}" has been deleted.'.format(user.username),
           category='success', action='delete_user')

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('main.index'))


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = get_or_404(User, id=id)
    form = EditUserForm(request.form, user)

    if form.validate_on_submit():
        if form.password.data:
            user.set_password(form.password.data)

        if form.role.data:
            user.role = form.role.data

        if form.username.data:
            user.username = form.username.data

        if form.email.data:
            user.email = form.email.data

        db.session.add(user)
        db.session.commit()

        notify(u'User "{0}" has been updated.'.format(user.username),
               category='success', action='edit_user')
        return redirect(url_for('users.view', id=id))

    return render_template('users/edit.html', user=user, form=form)
