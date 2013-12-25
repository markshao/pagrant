#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import os

from nose import main

from pagrant.basecommand import Command
from pagrant.commands.init import PAGRANT_CONFIG_FILE_NAME
from pagrant.environment import Environment
from pagrant.exceptions import PagrantConfigError, TestError


class TestCommand(Command):
    name = "test"
    usage = """%prog [options] """
    summary = "execute the test suites|cases with the options"

    def __init__(self):
        super(TestCommand, self).__init__()
        self.environment = None

    def run(self, args):
        if not os.path.exists(PAGRANT_CONFIG_FILE_NAME):
            raise PagrantConfigError(
                "The Pagrantfile should exist in the current folder , have to stop the test case execution")

        # validate the Pagrantfile config
        self.environment = Environment(os.path.abspath(PAGRANT_CONFIG_FILE_NAME), self.logger)

        self.logger.warn("start init the virtual environment for the test execution")
        self.environment.create_machines()
        self.environment.start_machines()
        self.logger.warn("finish init the virtual environment for the test execution")

        self.environment.init_test_context()

        try:
            main(args)
        except Exception, e:
            raise TestError(e.message)
        finally:
            self.environment.stop_machines()
            self.environment.destroy_machines()
