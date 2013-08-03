import re

from flask.ext.wtf import Form, ValidationError

from wtforms.ext.sqlalchemy.orm import model_form

from ..extensions import db

from .models import FUNCTION_NAME_REGEXP, Task


def task_code(form, field):
    functions_names_search = re.search(FUNCTION_NAME_REGEXP, field.data)

    if functions_names_search is None:
        raise ValidationError('Function name is not found.')

TaskForm = model_form(Task, db.session, Form, field_args={
    'code': {
        'validators': [task_code]
    }
})
