class Fabfile:
    """Fabfile class for generation fabfile"""

    def __init__(self, stage, tasks):
        self.__fabfile = self.__build(stage, tasks)

    def __build(self, stage, tasks):
        """Builds fabfile"""
        lines = []

        lines.extend(stage.project.code.split('\n'))
        lines.extend(stage.code.split('\n'))

        for task in stage.tasks:
            lines.extend(task.code.split('\n'))

        return lines

    def get(self):
        """Returns fabfile as string"""
        return '\n'.join(self.__fabfile)
