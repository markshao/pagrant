#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import os
from pagrant.basecommand import Command

PAGRANT_CONFIG_FILE_NAME = "Pagrantfile"


class InitCommand(Command):
    name = "init"
    usage = """%prog """
    summary = "help init the environment for the test"

    def __init__(self):
        pass

    def setup_logging(self):
        pass

    def run(self, args):
        pagrant_config_path = os.path.join(os.path.abspath(os.curdir), PAGRANT_CONFIG_FILE_NAME)

        # check the config whether already existed
        if os.path.exists(pagrant_config_path):
            need_create_new = raw_input("The Pagrantfile is existed , keep it ? (yes/no)")
        else:
            pass

    def _create_new_pagrant_file(self):
        pass