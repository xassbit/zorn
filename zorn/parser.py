import argparse
import sys

from zorn import tasks


def process_creation_request(args=None):
    """Simple helper to deal with the project creation command

    :param args: command line arguments
    """
    CreationParser(args).run()


def process_admin_request(args=None):
    """Simple helper to deal with project administration commands

    :param args: command line arguments
    """
    AdminParser(args).run()


class Parser:
    def __init__(self, args=None):
        """Wraps the argparse ArgumentParser with some helpful methods

        :param args: arguments from the command line
        """
        self._parser = argparse.ArgumentParser()
        self.task = None
        self.args = args
        self.task_arguments = {}
        self._parsed_args = None

    def add_arguments(self):
        """Register arguments to the parser"""
        self._parser.add_argument(
            '-v', '--verbose', action='store_true', help='make zorn talk more to you'
        )
        self._parser.add_argument(
            '-s', '--silent', action='store_true', help='(try to) silence zorn'
        )

    def parse_arguments(self):
        """Parse the arguments from the argument parser and set them as task arguments"""
        self._parsed_args = self._parser.parse_args(self.args)
        if self._parsed_args.silent is True:
            self.set_task_argument('verbosity', 0)
        elif self._parsed_args.verbose is True:
            self.set_task_argument('verbosity', 2)
        else:
            self.set_task_argument('verbosity', 1)

    def run_task(self):
        """Instantiate the task and runs it"""
        task = self.task(**self.task_arguments)
        task.run()

    def set_task_argument(self, arg, value):
        """Set arguments in the dictionary to be passed to the task object"""
        self.task_arguments[arg] = value

    def run(self):
        """Run all the necessary method to instanciate and configure the task and runs the task"""
        self.add_arguments()
        self.parse_arguments()
        self.run_task()


class CreationParser(Parser):
    def __init__(self, args=None):
        """Extend Parser

        The CreationParser can only trigger the `Create` task.

        :param args: arguments from the command line
        """
        super().__init__(args)
        self._parser.description = 'A tool for creation of zorn projects.'
        tasks_module = sys.modules['zorn.tasks']
        self.task = getattr(tasks_module, 'Create')

    def add_arguments(self):
        super().add_arguments()
        self._parser.add_argument(
            '-n', '--name', nargs='?', default=None, help='the name of the project (equal to its root directory)'
        )
        self._parser.add_argument(
            '-t', '--title', nargs='?', default=None, help='the title of the website'
        )
        self._parser.add_argument(
            '-a', '--author', nargs='?', default=None, help='the author of the website'
        )
        self._parser.add_argument(
            '--style', nargs='?', default=None, choices=tasks.Create.STYLES, help='the style to be imported'
        )
        self._parser.add_argument(
            '-g', '--generate', action='store_true',
            help='if true then generate the website at the end of project creation'
        )

    def parse_arguments(self):
        super().parse_arguments()
        self.set_task_argument('project_name', self._parsed_args.name)
        self.set_task_argument('site_title', self._parsed_args.title)
        self.set_task_argument('author', self._parsed_args.author)
        self.set_task_argument('style', self._parsed_args.style)
        self.set_task_argument('generate', self._parsed_args.generate)


class AdminParser(Parser):
    TASKS = {
        'generate': 'Generate',
        'importtemplates': 'ImportTemplates',
        'importstyle': 'ImportStyle',
    }

    def __init__(self, args=None):
        """Extend Parser

        AdminParser only runs tasks which concern an already created Zorn project.

        :param args:
        """
        super().__init__(args)
        self._parser.description = 'A tool for management of zorn projects.'
        self.update = False

    def add_arguments(self):
        super().add_arguments()

        def available_task(input_task):
            task = input_task.split(':')[0]
            if task not in AdminParser.TASKS:
                raise argparse.ArgumentTypeError(
                    'The task "{0}" was not recognized. Available tasks: {1}'.format(task, AdminParser.TASKS)
                )
            return input_task

        self._parser.add_argument('task', help='the admin task you wish to perform', type=available_task)
        self._parser.add_argument(
            '-u', '--update', action='store_true', help='update settings after task is run (if applicable)'
        )

    def parse_arguments(self):
        super().parse_arguments()
        tasks_module = sys.modules['zorn.tasks']
        input_task = self._parsed_args.task
        if ':' in str(input_task):
            input_task = input_task.split(':')
            self.task = getattr(tasks_module, AdminParser.TASKS[input_task[0]])
            self.set_task_argument('task_args', input_task[1:])
        else:
            self.task = getattr(tasks_module, AdminParser.TASKS[input_task])
        self.set_task_argument('update', self._parsed_args.update)
