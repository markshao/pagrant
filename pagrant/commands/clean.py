#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import os
from pagrant.basecommand import Command
from pagrant.commands import PAGRANT_CONFIG_FILE_NAME, MACHINES_PERSISTENT_FILE
from pagrant.environment import Environment
from pagrant.exceptions import PagrantError, PagrantConfigError


class CleanCommand(Command):
    name = "clean"
    usage = """%prog """
    summary = "clean the entire test environment"

    def __init__(self):
        super(CleanCommand, self).__init__()

    def setup_logging(self):
        pass

    def run(self, args):
        if not os.path.exists(PAGRANT_CONFIG_FILE_NAME):
            raise PagrantConfigError(
                "The Pagrantfile should exist in the current folder , have to stop the test case execution")

        # validate the Pagrantfile config
        self.environment = Environment(os.path.abspath(PAGRANT_CONFIG_FILE_NAME), self.logger)

        try:
            if not os.path.exists(MACHINES_PERSISTENT_FILE):
                raise PagrantError("Could clean the environment")
            self.environment.clean_from_persistent(MACHINES_PERSISTENT_FILE)
        except PagrantError, e:
            raise e