__author__ = 'root'

from pagrant.basecommand import Command


class ListCommand(Command):
    name = "list"
    usage = """%prog """
    summary = "help init the environment for the test"

    def __init__(self):
        super(ListCommand,self).__init__()