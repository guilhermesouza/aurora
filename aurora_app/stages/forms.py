from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

from ..extensions import db

from .models import Stage

StageForm = model_form(Stage, db.session, Form)
