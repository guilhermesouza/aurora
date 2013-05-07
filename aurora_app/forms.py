from flask.ext.wtf import (Form, Required, TextField, BooleanField,
                           PasswordField)

from wtforms.ext.sqlalchemy.orm import model_form
from aurora_app.models import Stage, Project, Task
from aurora_app.database import db


class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me', default=False)

ProjectForm = model_form(Project, db.session, Form)
StageForm = model_form(Stage, db.session, Form)
TaskForm = model_form(Task, db.session, Form)
