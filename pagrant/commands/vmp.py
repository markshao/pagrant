#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys
from pagrant.basecommand import Command
from pagrant.vmproviders import providers


class VmpCommand(Command):
    """
        The vmprovider is used to manage all the vm providers
    """
    name = "vmprovider"
    usage = """%prog [options]"""
    summary = "display all the providers support by the pagrant , but you can extend it by your selves"

    def __init__(self):
        # first init the base class
        super(VmpCommand, self).__init__()
        self.left_length = 30

    def setup_logging(self):
        pass

    def run(self, args):
        sys.stdout.write("VM Providers list:\n")
        for name, summary in providers.items():
            sys.stdout.write(" " * 3)
            sys.stdout.write(name)
            sys.stdout.write(" " * self._calc_space(name))
            sys.stdout.write("%s\n" % summary)

    def _calc_space(self, name):
        return self.left_length - 3 - len(name)
