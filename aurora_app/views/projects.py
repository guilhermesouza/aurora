from flask import Blueprint, render_template

from aurora_app.constants import ROLES
from aurora_app.decorators import requires_login, need_to_be
from aurora_app.forms import CreateProjectForm

mod = Blueprint('projects', __name__, url_prefix='/projects')


@mod.route('/create')
@requires_login
@need_to_be(role=ROLES['ADMIN'])
def create():
    form = CreateProjectForm()
    return render_template('projects/create.html', form=form)
