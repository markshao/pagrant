#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.pagrantfile import ContextConfig

# each test contains a environment for test


class Environment(object):
    def __init__(self, pagrantfile_path):
        self.pagrantfile_path = pagrantfile_path
        self.context_config = ContextConfig(self.pagrantfile_path)

        self.context_config.get_vmprovider_type()