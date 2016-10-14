import importlib
import os

import sys

import zorn.elements


def process_request(args):
    try:
        # Register commands here
        if args[1] == 'generate':
            return Generate(args)
    except Exception as e:
        sys.exit(CliColors.ERROR + str(e) + CliColors.RESET)


class UnrecognizedFlagError(Exception):
    pass

class CliColors:
    HEADER = '\033[32m'
    MAIN = '\033[36m'
    ERROR = '\033[1;31m'
    SUCESS = '\033[1;32m'
    RESET = '\033[0m'

class Command:
    _available_flags = []

    def __init__(self, args):
        self.name = args[1]
        self.flags = [flag for flag in args if flag[0] == '-']
        for flag in self.flags:
            if flag not in Command._available_flags:
                raise UnrecognizedFlagError(
                    "I'm afraid the flag {0} is not recognized.".format(flag)
                )
        if len(args) > 2:
            self.args = [arg for arg in args[2:] if arg[0] != '-']

        print(CliColors.HEADER + '\nWelcome to zorn!\n')


class Generate(Command):
    _available_flags = []

    @staticmethod
    def process_settings():

        module = importlib.import_module(os.environ['ZORN_SETTINGS'])
        settings = {}
        for setting in module.__dict__.keys():
            if setting.upper() == setting:
                settings[setting.lower()] = module.__dict__[setting]

        return settings

    def __init__(self, args):
        super().__init__(args)
        print(CliColors.MAIN + 'Generating... \n')
        try:
            website = zorn.elements.Website(self.process_settings())
            website.generate_pages()
        except Exception as e:
            sys.exit(CliColors.ERROR + str(e) + CliColors.RESET)
        print(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
