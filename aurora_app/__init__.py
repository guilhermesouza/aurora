from __future__ import absolute_import
import os

from celery import Celery
from flask import Flask, render_template, url_for, g, request, redirect
from flask.ext.login import LoginManager, current_user
from flask.ext.debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object('settings')
app.threaded = True
app.processes = 5

# Celery
celery = Celery(app)
celery.add_defaults(app.config)

from aurora_app.tasks import *

# Enable login manager extension
login_manager = LoginManager()
login_manager.setup_app(app)

# Enable debug toolbar
toolbar = DebugToolbarExtension(app)

# Make Aurora folder if not exists
from aurora_app.helpers import create_aurora_folder
create_aurora_folder(app.config['AURORA_PATH'])


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    from aurora_app.database import db
    db.session.rollback()
    return render_template('500.html'), 500


@app.before_request
def check_login():
    g.user = current_user if current_user.is_authenticated() else None

    if (request.endpoint and request.endpoint != 'static' and
       (not getattr(app.view_functions[request.endpoint], 'is_public', False)
       and g.user is None)):
        return redirect(url_for('main.login', next=request.path))


# To exclude caching of static
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


from aurora_app.views import main, projects, stages, tasks, notifications

app.register_blueprint(main.mod)
app.register_blueprint(projects.mod)
app.register_blueprint(stages.mod)
app.register_blueprint(tasks.mod)
app.register_blueprint(notifications.mod)

# Enable context processors
from aurora_app.context_processors import projects, notifications
