#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from fabric.api import settings
from fabric.operations import run


class FabricSupport(object):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def execute_shell_command(self, command):
        with settings(host_string=self.host, user=self.username, password=self.password):
            return run(command, shell=True)

