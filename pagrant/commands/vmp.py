#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.basecommand import Command


class VmpCommand(Command):
    """
        The vmp is used to manage the vm providers which
        has been installed in the current pagrant framework
    """
    name = "vmprovider"
    usage = """%prog [options]"""
    summary = "vmprovider"

    def __init__(self):
        # first init the base class
        super(VmpCommand, self).__init__()


    def setup_logging(self):
        pass


