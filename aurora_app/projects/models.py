import os

from git import Repo
from flask import current_app

from ..extensions import db
from ..stages.models import Stage

from .constants import DEFAULT_PARAMETERS, PARAMETER_TYPES
from .exceptions import ParameterValueError


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128), default='')
    repository_path = db.Column(db.String(128), default='')
    code = db.Column(db.Text(), default='')
    # Relations
    stages = db.relationship(Stage, backref="project")
    params = db.relationship("ProjectParameter", backref="project")

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def create_default_params(self):
        for parameter_name in DEFAULT_PARAMETERS.keys():
            self.create_default_parameter(parameter_name)

    def create_default_parameter(self, name):
        parameter_dict = DEFAULT_PARAMETERS[name]
        parameter_dict['name'] = name
        parameter_dict['project_id'] = self.id
        parameter = ProjectParameter(**parameter_dict)
        db.session.add(parameter)
        db.session.commit()
        return parameter

    def get_or_create_parameter_value(self, name):
        for parameter in self.params:
            if parameter.name == name:
                return parameter.value

        return self.create_default_parameter(name).value

    def get_name_for_path(self):
        return self.name.lower().replace(' ', '_')

    def get_path(self):
        """Returns path of project's git repository on local machine."""
        return os.path.join(current_app.config['AURORA_PROJECTS_PATH'],
                            self.get_name_for_path())

    def repository_folder_exists(self):
        return os.path.exists(self.get_path())

    def get_repo(self):
        if self.repository_folder_exists():
            return Repo.init(self.get_path())
        return None

    def get_branches(self):
        repo = self.get_repo()
        if repo:
            return [ref for ref in repo.refs if ref.name != 'origin/HEAD']
        return None

    def get_commits(self, branch, max_count, skip):
        repo = self.get_repo()
        if repo:
            return repo.iter_commits(branch, max_count=max_count,
                                     skip=skip)
        return None

    def get_all_commits(self, branch, skip=None):
        repo = self.get_repo()
        if repo:
            return repo.iter_commits(branch, skip=skip)
        return None

    def get_last_commit(self, branch):
        repo = self.get_repo()
        if repo:
            return repo.iter_commits(branch).next()
        return None

    def get_commits_count(self, branch):
        repo = self.get_repo()
        if repo:
            return reduce(lambda x, _: x + 1, repo.iter_commits(branch), 0)
        return None

    def fetch(self):
        repo = self.get_repo()
        if repo:
            return repo.git.fetch()

    def __repr__(self):
        return self.name


class ProjectParameter(db.Model):
    __tablename__ = "project_parameters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    value = db.Column(db.String(128), nullable=False)
    type = db.Column(db.SmallInteger, nullable=False)
    # Relations
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'),
                           nullable=False)

    def set_value(self, value):
        if self.type == PARAMETER_TYPES['BOOL']:
            values = ['True', 'False']
            if value not in values:
                raise ParameterValueError('Wrong value for bool parameter.')
        elif self.type == PARAMETER_TYPES['INT']:
            try:
                int(value)
            except ValueError:
                raise ParameterValueError('Wrong value for int parameter.')

        self.value = value

    def __init__(self, *args, **kwargs):
        super(ProjectParameter, self).__init__(*args, **kwargs)
