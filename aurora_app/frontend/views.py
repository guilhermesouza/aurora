from flask import Blueprint, render_template, redirect, g, url_for, request
from flask.ext.login import login_user, logout_user, current_user

from ..decorators import public
from ..users.models import User
from ..deployments.models import Deployment

from .forms import LoginForm

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    deployments = Deployment.query.order_by('started_at desc').limit(10).all()
    return render_template('frontend/index.html', deployments=deployments)


@frontend.route('/login', methods=['GET', 'POST'])
@public
def login():
    if g.user is not None:
        return redirect(url_for('frontend.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.email.data,
                                                form.password.data)
        if user and authenticated:
            if login_user(user, remember=form.remember_me.data):
                return redirect(request.args.get('next') or
                                url_for('frontend.index'))

        form.password.errors = [u'Invalid password.']

    return render_template('frontend/login.html', form=form)


@frontend.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('frontend.index'))
