#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import imp
from pagrant.exceptions import PagrantConfigError

PAGRANTFILE_MODULE = "Pagrantfile"


class ContextConfig(object):
    def __init__(self, pagrantfile_path):
        try:
            self.pagrantfile_path = pagrantfile_path
            self.pagrant_file_module = imp.load_source(PAGRANTFILE_MODULE, self.pagrantfile_path)
        except ImportError:
            raise PagrantConfigError("Could not import the Pagrantfile, please check the syntax of the file")

        self.validate()  # keep the file should work

    def validate(self):
        required = ['machine_settings', 'vmprovider_config', 'vmprovider']
        print
        for key in required:
            if key not in dir(self.pagrant_file_module):
                raise PagrantConfigError("The config not contains the element config %s" % key)