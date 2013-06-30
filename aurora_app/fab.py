import imp


class Fabfile:
    """Class for building fabfile"""
    def __init__(self, stage, tasks):
        self.module = imp.new_module("aurora_sandbox")
        self.__build(stage)
        self.__tasks_to_run = tasks

    def __build(self, stage):
        """Builds fabfile"""
        content = stage.project.code + "\n" + stage.code + "\n"

        for task in stage.tasks:
            content += task.code + "\n"

        exec content in self.module.__dict__

    def run(self):
        for task in self.__tasks_to_run:
            name = task.get_function_name()
            try:
                eval('self.module.' + name)()
            except Exception as e:
                # handle
                pass
