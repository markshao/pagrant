#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.vmproviders import lxc
from pagrant.exceptions import VirtualBootstrapError


providers = {
    lxc.provider_name: lxc.privider_summary,
}


class BaseProvider(object):
    def __init__(self, provider_info, logger):
        self.logger = logger
        self.provider_info = provider_info

    def _create_machines(self, machine_settings):
        NotImplemented

    def create_machines(self, machine_settings):
        try:
            self._create_machines(machine_settings)
        except Exception, e:
            raise VirtualBootstrapError(str(e))


from pagrant.vmproviders.lxc.actions import LxcProvider

providers_class_map = {
    lxc.provider_name: LxcProvider
}

