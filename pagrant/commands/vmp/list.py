__author__ = 'root'

import sys
import os
from pagrant.basecommand import Command
from pagrant.vmproviders import providers


DEFAULT_BLANK = 30


class ListCommand(Command):
    name = "list"
    usage = """%prog """
    summary = "help init the environment for the test"

    def __init__(self):
        super(ListCommand, self).__init__()

    def setup_logging(self):
        pass

    def run(self, args):
        sys.stdout.write("pagrant native support list:")
        sys.stdout.write(os.linesep)
        for k, v in providers.items():
            sys.stdout.write(" " * 6)
            sys.stdout.write(k)
            self._print_blank(k)
            sys.stdout.write(v)
            sys.stdout.write(os.linesep)

    def _print_blank(self, k):
        need_blank = DEFAULT_BLANK - len(k)
        sys.stdout.write(" " * need_blank)


