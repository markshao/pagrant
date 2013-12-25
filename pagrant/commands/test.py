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

        self.logger.warn("start running the test cases ... \n")

        self.logger.warn("start create the vms ...")
        self.environment.create_machines()
        self.logger.warn("finish create the vms")

        self.logger.warn("start bootstrap the vms ...")
        self.environment.start_machines()
        self.logger.warn("finish boostrap the vms")

        try:
            main(args)
        except Exception, e:
            raise TestError(e.message)
        finally:
            self.logger.warn("start stop all the machines")
            self.environment.stop_machines()
            self.logger.warn("finish stop all the machiines")

            self.logger.warn("start destroy all the machines")
            self.environment.destroy_machines()
            self.logger.warn("finish destroy all the machiines")
