__author__ = 'root'

from pagrant.basecommand import Command


class InstallCommand(Command):
    name = "install"
    usage = """%prog """
    summary = "help init the environment for the test"

    def __init__(self):
        super(InstallCommand, self).__init__()
