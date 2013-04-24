from flask.ext.wtf import (Form, Required, TextField, BooleanField,
                           PasswordField, TextAreaField)


class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me', default=False)


class ProjectForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextAreaField('Description')
    repo_path = TextField("Git repo's path")
