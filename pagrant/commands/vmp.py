#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.basecommand import Command


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

    def setup_logging(self):
        pass

    def run(self, args):
        pass


class VmpBaseSubcommand(object):
    def __init__(self):
        pass