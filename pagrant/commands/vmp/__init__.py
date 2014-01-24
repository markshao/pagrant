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
from pagrant.exceptions import CommandError, PagrantError


class VmpCommand(Command):
    name = "vmprovider"
    usage = """%prog [command] [options]"""
    summary = "vmproviers management command , plese use [pagrant vmprovider --help] to see the detail usage"
    skip_parse = True

    def __init__(self):
        super(VmpCommand, self).__init__()

        # create command listing for description
        command_summaries = get_summaries()
        description = [''] + ['%-27s %s' % (i, j) for i, j in command_summaries]
        self.parser.description = '\n'.join(description)
        self.parser.main = True  # so the help formatter knows

        self.skip_parse = True


    def setup_logging(self):
        pass

    def run(self, args):

        if not args or (args[0].lower() == 'help' and len(args) == 1):
            self.parser.print_help()
            sys.exit()

        # the subcommand name
        cmd_name = args[0].lower()

        if cmd_name not in commands:
            raise CommandError("The command {} is not support by the vmprovider".format(cmd_name))

        #all the args without the subcommand
        cmd_args = args[:]
        cmd_args.remove(args[0].lower())

        command = commands[cmd_name]()
        command.logger = self.logger # copy the logger from outside -> inside
        try:
            command.run(cmd_args)
        except PagrantError, error:
            pass


# The following code is used for handling the third party vmproviders

import os
from pagrant.globalsettings import VMPROVIDER_LIST_DICT
from pagrant.util import read_dict_fd, write_json_fd


def check_vmprovider_file():
    return os.path.exists(VMPROVIDER_LIST_DICT)


def check_vmprovider_existed(vmprovider_name):
    if check_vmprovider_file():
        current_vm_dict = read_dict_fd(VMPROVIDER_LIST_DICT)
        return vmprovider_name in current_vm_dict
    else:
        return False


def get_installed_vmproviders():
    if check_vmprovider_file():
        return read_dict_fd(VMPROVIDER_LIST_DICT)
    else:
        return {}


def add_into_vmprovider_dict(vmprovider_name, **kwargs):
    dist = get_installed_vmproviders()
    dist[vmprovider_name] = kwargs
    write_json_fd(dist, VMPROVIDER_LIST_DICT)


def remove_vmprovider_dict(vmprovider_name):
    dist = get_installed_vmproviders()
    if vmprovider_name in dist:
        del dist[vmprovider_name]
    write_json_fd(dist, VMPROVIDER_LIST_DICT)


# ENTRY_POINT REALTED
EP_GROUP = "PAGRANT"
EP_NAME = "VMPROVIDER   "

# solve the loop import issue
from pagrant.commands.vmp.list import ListCommand
from pagrant.commands.vmp.install import InstallCommand
from pagrant.commands.vmp.remove import RemoveCommand

commands = {
    ListCommand.name: ListCommand,
    InstallCommand.name: InstallCommand,
    RemoveCommand.name: RemoveCommand
}


def get_summaries(ignore_hidden=True):
    """Yields sorted (command name, command summary) tuples."""

    cmditems = commands.items()

    for name, command_class in cmditems:
        if ignore_hidden and command_class.hidden:
            continue
        yield (name, command_class.summary)