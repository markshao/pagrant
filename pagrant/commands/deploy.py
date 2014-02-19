#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import os
from pagrant.basecommand import Command
from pagrant.commands import PAGRANT_CONFIG_FILE_NAME, MACHINES_PERSISTENT_FILE
from pagrant.environment import Environment
from pagrant.exceptions import PagrantError, PagrantConfigError
from pagrant.version import version_number


class DeployCommand(Command):
    name = "deploy"
    usage = """%prog """
    summary = "deploy the test environment base on the Pagrantfile"

    def __init__(self):
        super(DeployCommand, self).__init__()
        self.environment = None

    def setup_logging(self):
        pass

    def run(self, args):
        if not os.path.exists(PAGRANT_CONFIG_FILE_NAME):
            raise PagrantConfigError(
                "The Pagrantfile should exist in the current folder , have to stop the test case execution")

        # validate the Pagrantfile config
        self.environment = Environment(os.path.abspath(PAGRANT_CONFIG_FILE_NAME), self.logger)

        self.print_context_log()
        self.environment.create_machines()
        self.environment.start_machines()
        self.logger.info("finish create the test environment")

        try:
            # the init is always needed
            self.environment.init_test_context()
            self.environment.check_machine_ssh()

            self.logger.info("start provision the environment")
            self.environment.provision_environment()
            self.logger.info("Done!")

            if os.path.exists(MACHINES_PERSISTENT_FILE):
                os.remove(MACHINES_PERSISTENT_FILE)
            self.environment.persistent_to_path(MACHINES_PERSISTENT_FILE)

            self.logger.info("persistent the machine informations")
        except PagrantError, e:
            raise e

    def print_context_log(self):
        self.logger.info("pagrant version %s" % version_number())
        self.logger.info("using vmprovider [%s]" % self.environment.vmprovider_type)
        self.logger.info(
            "create the test environment with the machines %s" % self.environment.machines_info.keys())