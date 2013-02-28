from django.template.loader import render_to_string

import os


class Fabfile:
    """Fabfile class for generation fabfile"""

    def __init__(self, imports, tasks, path,
                 env_params={}):
        self.__imports = imports
        self.__tasks = tasks
        self.__file_path = path
        self.__env_params = env_params

    def _imports_block(self):
        """imports block"""
        return self.__imports

    def _params(self):
        """env params"""
        return self.__env_params.items()

    def _tasks(self):
        """tasks block"""
        return self.__tasks

    def _file_path(self):
        """File dir"""
        return self.__file_path

    def _file_content(self):
        """generate and return fabfile content"""
        context = {'imports': self._imports_block(),
                   'params': self._params(),
                   'tasks': self._tasks()}
        return render_to_string('fabfile.template', context)

    def file_name(self):
        """Full file name"""
        return "%s/fabfile.py" % self._file_path()

    def build(self):
        """build fabfile and save to file_path"""
        if not os.path.exists(self._file_path()):
            os.makedirs(self._file_path())

        with open(self.file_name(), 'w') as f:
            f.write(self._file_content())
