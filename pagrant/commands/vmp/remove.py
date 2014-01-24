__author__ = 'root'

from pip import main
from pagrant.basecommand import Command
from pagrant.exceptions import CommandError
from pagrant.commands.vmp import remove_vmprovider_dict


class RemoveCommand(Command):
    name = "remove"
    usage = """%prog """
    summary = "remove the specific vmprovider"

    def __init__(self):
        super(RemoveCommand, self).__init__()

    def run(self, args):
        options, arg_else = self.parse_args(args)

        if not arg_else or len(arg_else) != 1:
            raise CommandError("the vmprovider name is empty , could install it \n")

        remove_commands = ["uninstall", arg_else[0], "-y"]

        self.logger.warn("start remove the vmprovider [{}]".format(arg_else[0]))
        main(remove_commands)
        remove_vmprovider_dict(arg_else[0])
        self.logger.warn("finish remove the new provider")
