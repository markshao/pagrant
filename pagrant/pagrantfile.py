#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import imp
import os

from pagrant.exceptions import PagrantConfigError


PAGRANTFILE_MODULE = "Pagrantfile"
PAGRANTFILE_MODULE_COMPILE_PATH = os.path.join(os.path.curdir, "Pagrantfilec")


class ContextConfig(object):
    def __init__(self, pagrantfile_path):
        try:
            self.pagrantfile_path = pagrantfile_path
            self.pagrant_file_module = imp.load_source(PAGRANTFILE_MODULE, self.pagrantfile_path)

            os.remove(PAGRANTFILE_MODULE_COMPILE_PATH)
        except ImportError:
            raise PagrantConfigError("Could not import the Pagrantfile, please check the syntax of the file")

        self.validate()  # keep the file should work

    def validate(self):
        required = ['machine_settings', 'vmprovider_config', 'vmprovider']
        print
        for key in required:
            if key not in dir(self.pagrant_file_module):
                raise PagrantConfigError("The config not contains the element config %s" % key)

    def get_machine_settings(self):
        machine_settings = self.pagrant_file_module.machine_settings()
        return machine_settings

    def get_vmprovider_type(self):
        vmprovider_type = self.pagrant_file_module.vmprovider
        #         if vmprovider_type not in providers:
        #             raise PagrantConfigError("""
        # The vmprovider is not support by the pagrant right\n
        # Please first check the vmprovider list through the command: pagrant vmprovider\n""")

        return vmprovider_type

    def get_vmprovider_config(self):
        return self.pagrant_file_module.vmprovider_config()

    def get_vmprovider(self):
        return self.pagrant_file_module.vmprovider()