#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.pagrantfile import ContextConfig
from pagrant.vmproviders import providers_class_map

# each test contains a environment for test


class Environment(object):
    def __init__(self, pagrantfile_path, logger):
        self.pagrantfile_path = pagrantfile_path
        self.context_config = ContextConfig(self.pagrantfile_path)

        self.logger = logger

        # decide the vmprovider to user
        vmprovider_type = self.context_config.get_vmprovider_type()
        vmprovider_class = providers_class_map.get(vmprovider_type)
        self._vmprovider = vmprovider_class(self.context_config.get_vmprovider_config(), self.logger)
        self.machines_info = {}

    @property
    def vmprovider(self):
        return self._vmprovider

    def create_machines(self):
        self._vmprovider.create_machines(self.context_config.get_machine_settings())
