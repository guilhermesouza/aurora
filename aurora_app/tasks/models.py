import re

from ..extensions import db

FUNCTION_NAME_REGEXP = '^def (\w+)\(.*\):'


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    code = db.Column(db.Text(), default='')

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def get_function_name(self):
        functions_search = re.search(FUNCTION_NAME_REGEXP, self.code)
        return functions_search.group(1)

    def __repr__(self):
        return self.name
