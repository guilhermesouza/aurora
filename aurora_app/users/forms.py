from flask.ext.wtf import (Form, Email, Required, TextField, PasswordField,
                           SelectField)

from .constants import ROLES


class EditUserForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password')
    email = TextField('Email', validators=[Email()])
    role = SelectField(u'Role', coerce=int,
                       choices=[(v, k) for k, v in ROLES.iteritems()])


class CreateUserForm(EditUserForm):
    password = PasswordField('Password', validators=[Required()])
