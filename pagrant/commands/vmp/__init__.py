__author__ = 'root'

"""
    The vmprovider will support the following commands

    vmprovider list
        -- list all the provider [native support + third party installed]

    vmprovider install [vmprovider name]
        -- install the new vmprovider from pypi
"""

import sys

from pagrant.basecommand import Command
from pagrant.exceptions import CommandError


class VmpCommand(Command):
    name = "vmprovider"
    usage = """%prog [command] [options]"""
    summary = "help init the environment for the test"

    def __init__(self):
        super(VmpCommand, self).__init__()

        # create command listing for description
        command_summaries = get_summaries()
        description = [''] + ['%-27s %s' % (i, j) for i, j in command_summaries]
        self.parser.description = '\n'.join(description)
        self.parser.main = True  # so the help formatter knows


    def setup_logging(self):
        pass

    def run(self, args):
        options, args_else = self.parse_args(args)

        if not args_else or (args_else[0].lower() == 'help' and len(args_else) == 1):
            self.parser.print_help()
            sys.exit()

        # the subcommand name
        cmd_name = args[0].lower()

        if cmd_name not in commands:
            raise CommandError("The command {} is not support by the vmprovider".format(cmd_name))

        #all the args without the subcommand
        cmd_args = args[:]
        cmd_args.remove(args_else[0].lower())

        command = commands[cmd_name]()
        try:
            command.run(cmd_args)
        except Exception, ex:
            pass


# solve the loop import issue
from pagrant.commands.vmp.list import ListCommand
from pagrant.commands.vmp.install import InstallCommand

commands = {
    ListCommand.name: ListCommand,
    InstallCommand.name: InstallCommand
}


def get_summaries(ignore_hidden=True):
    """Yields sorted (command name, command summary) tuples."""

    cmditems = commands.items()

    for name, command_class in cmditems:
        if ignore_hidden and command_class.hidden:
            continue
        yield (name, command_class.summary)