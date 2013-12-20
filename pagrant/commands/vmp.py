#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys
from pagrant.basecommand import Command


class VmpCommand(Command):
    """
        The vmprovider is used to manage all the vm providers
    """
    name = "vmprovider"
    usage = """%prog [options]"""
    summary = "vmprovider"

    def __init__(self):
        # first init the base class
        super(VmpCommand, self).__init__()

    def setup_logging(self):
        pass

    def run(self, args):
        option, args_else = self.parser.parse_args(args)

        if not args_else or (args_else[0].lower() == 'help' and len(args_else) == 1):
            self.parser.print_help()
            sys.exit()