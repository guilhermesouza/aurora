import os

from flask import Flask, render_template, url_for, g
from flask.ext.login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('settings')

# Enable login manager extension
login_manager = LoginManager()
login_manager.setup_app(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.before_request
def before_request():
    g.user = current_user if current_user.is_authenticated() else None


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


from aurora_app.views import main
from aurora_app.views import projects

app.register_blueprint(main.mod)
app.register_blueprint(projects.mod)

# Enable context processors
from aurora_app.context_processors import projects
