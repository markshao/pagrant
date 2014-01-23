__author__ = 'root'

import sys
import os
from pagrant.basecommand import Command
from pagrant.vmproviders import providers
from pagrant.commands.vmp import get_installed_vmproviders


DEFAULT_BLANK = 30


class ListCommand(Command):
    name = "list"
    usage = """%prog """
    summary = "list all the installed vmproviders"

    def __init__(self):
        super(ListCommand, self).__init__()

    def run(self, args):
        self.parse_args(args)  # WORK AROUND

        sys.stdout.write("Native supported List:")
        sys.stdout.write(os.linesep)
        for k, v in providers.items():
            sys.stdout.write(" " * 6)
            sys.stdout.write(k)
            self._print_blank(k)
            sys.stdout.write(v)
            sys.stdout.write(os.linesep)

            # third party
        sys.stdout.write(os.linesep)
        sys.stdout.write("Third-party installed List:")
        sys.stdout.write(os.linesep)

        for k, v in get_installed_vmproviders().items():
            sys.stdout.write(" " * 6)
            sys.stdout.write(k)
            self._print_blank(k)
            sys.stdout.write(v.get("summary", "nothing"))
            sys.stdout.write(os.linesep)


    def _print_blank(self, k):
        need_blank = DEFAULT_BLANK - len(k)
        sys.stdout.write(" " * need_blank)


