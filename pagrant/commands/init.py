#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import sys
import shutil

import os
from pagrant.commands import PAGRANT_CONFIG_FILE_NAME
from pagrant.basecommand import Command
from pagrant.util import get_userinput, is_true
from pagrant.globalsettings import PAGRANT_CONFIG_TEMPLATE_PATH


class InitCommand(Command):
    name = "init"
    usage = """%prog """
    summary = "init the Pagrantfile for the test"

    def __init__(self):
        super(InitCommand, self).__init__()

    def setup_logging(self):
        pass

    def run(self, args):
        pagrant_config_path = os.path.join(os.path.abspath(os.curdir), PAGRANT_CONFIG_FILE_NAME)

        # check the config whether already existed
        if os.path.exists(pagrant_config_path):
            resp = get_userinput("The Pagrant has already existed,do you need to overide it ? (yes/no):")
            if is_true(resp):
                self._create_new_pagrant_file(pagrant_config_path)
            else:
                self.logger.fatal("The new Pagrantfile is not created. Keep using the old one \n")
        else:
            self._create_new_pagrant_file(pagrant_config_path)

    def _create_new_pagrant_file(self, pagrant_config_path):
        if os.path.exists(pagrant_config_path):
            os.remove(pagrant_config_path)
        shutil.copy(PAGRANT_CONFIG_TEMPLATE_PATH, pagrant_config_path)

        # add the message for the new creation of pagrantfile
        sys.stdout.write("The new Pagrantfile has been created. \n")
