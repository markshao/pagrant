#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.basecommand import Command


class VmpCommand(Command):
    """
        The vmp is used to manage the vm providers which
        has been installed in the current pagrant framework
    """
    name = "vmp"
    usage = """%prog [options]"""
    summary = "vmp"

    def setup_logging(self):
        pass


