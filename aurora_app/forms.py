from flask.ext.wtf import Form, Required, TextField, BooleanField, PasswordField


class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)
