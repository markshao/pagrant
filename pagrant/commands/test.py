#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import os

from nose import main

from pagrant.vendors.myoptparser.optparse import Option
from pagrant.basecommand import Command
from pagrant.commands.init import PAGRANT_CONFIG_FILE_NAME
from pagrant.environment import Environment
from pagrant.exceptions import PagrantConfigError, TestError


class TestCommand(Command):
    name = "test"
    usage = """%prog [options] [nose-options]"""
    summary = "execute the test suites|case with the options"

    def __init__(self):
        super(TestCommand, self).__init__()
        self.parser.add_option(Option(
            # Writes the log levels explicitely to the log'
            '--newvm',
            dest='newvm',
            action='store_true',
            default=False,
            help="if set --newvm , the test will fisrt create the new vm against " \
                 "the Pagrantfile and destroy them after test"
        ))
        self.environment = None

    def run(self, args):
        if not os.path.exists(PAGRANT_CONFIG_FILE_NAME):
            raise PagrantConfigError(
                "The Pagrantfile should exist in the current folder , have to stop the test case execution")

        # validate the Pagrantfile config
        self.environment = Environment(os.path.abspath(PAGRANT_CONFIG_FILE_NAME), self.logger)

        # deal with the parameter
        newvm = True if "--newvm" in args and args[0] == "--newvm" else False

        # currently is a work round
        if "--newvm" in args and not args[0] == "--newvm":
            raise PagrantConfigError("The --newvm should before the nose test parameters")

        nose_args = args[1:] if newvm else args

        if newvm:
            self.logger.warn("start init the virtual environment for the test execution")
            self.environment.create_machines()
            self.environment.start_machines()
            self.logger.warn("finish init the virtual environment for the test execution")

        # the init is always needed
        self.environment.init_test_context()

        try:
            main(nose_args)
        except Exception, e:
            raise TestError("The nose test exception --- %s \n" % e.message)
        finally:
            if newvm:
                self.environment.stop_machines()
                self.environment.destroy_machines()
