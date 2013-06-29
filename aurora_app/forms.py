import re

from flask.ext.wtf import (Form, Required, TextField, BooleanField,
                           PasswordField, ValidationError)

from wtforms.ext.sqlalchemy.orm import model_form

from aurora_app.models import Stage, Project, Task, FUNCTION_NAME_REGEXP
from aurora_app.database import db


def task_code(form, field):
    functions_names_search = re.search(FUNCTION_NAME_REGEXP, field.data)

    if functions_names_search is None:
        raise ValidationError('Function name is not found.')


class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me', default=False)

ProjectForm = model_form(Project, db.session, Form)
StageForm = model_form(Stage, db.session, Form)
TaskForm = model_form(Task, db.session, Form, field_args={
    'code': {
        'validators': [task_code]
    }
})
