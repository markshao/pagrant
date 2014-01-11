__author__ = 'root'

from pip import main
from pagrant.basecommand import Command
from pagrant.vendors.myoptparser.optparse import Option
from pagrant.exceptions import CommandError


class InstallCommand(Command):
    name = "install"
    usage = """%prog """
    summary = "help init the environment for the test"

    def __init__(self):
        super(InstallCommand, self).__init__()
        self.parser.add_option(Option(
            '--index-url',
            dest='index_url',
            action='store',
            default=None,
            help="change the source for the vmprovider existed"
        ))

    def run(self, args):
        options, arg_else = self.parse_args(args)

        if not arg_else or len(arg_else) != 1:
            raise CommandError("the vmprovider name is empty , could install it \n")

        install_commands = ["install", arg_else[0]]

        if options.index_url:
            install_commands.extend(["--index-url", options.index_url])

        self.logger.warn("start install the vmprovider [{}]".format(arg_else[0]))
        main(install_commands)
        self.logger.warn("finish install the new provider")
