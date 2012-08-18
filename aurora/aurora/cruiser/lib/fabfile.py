from django.template.loader import render_to_string


class Fabfile:
    """Fabfile class for generation fabfile"""

    def __init__(self, imports, tasks, path,
                 env_params={}):
        self.__imports = imports
        self.__tasks = tasks
        self.__file_path = path
        self.__env_params = env_params

    def imports_block(self):
        """imports block"""
        return self.__imports

    def params(self):
        """env params"""
        return self.__env_params.items()

    def tasks(self):
        """tasks block"""
        return self.__tasks

    def file_name(self):
        """Full file name"""
        return "%s/fabfile.py" % self.__file_path

    def file_content(self):
        """generate and return fabfile content"""
        context = {'imports': self.imports_block(),
                   'params': self.params(),
                   'tasks': self.tasks()}
        return render_to_string('fabfile.template', context)

    def build(self):
        """build fabfile and save to file_path"""
        with open(self.file_name(), 'w') as f:
            f.write(self.file_content())