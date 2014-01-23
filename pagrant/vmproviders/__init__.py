#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.vmproviders import lxc


providers = {
    lxc.provider_name: lxc.privider_summary,
}


class BaseProvider(object):
    def __init__(self, provider_info, logger):
        self.logger = logger
        self.provider_info = provider_info

    def create_machines(self, machine_settings):
        NotImplemented

    def start_machines(self, machine_settings):
        NotImplemented

    def stop_machines(self, machine_settings):
        NotImplemented

    def destroy_machines(self, machine_settings):
        NotImplemented

    def get_machine_ip(self, machine_setting):
        NotImplemented


from pagrant.vmproviders.lxc.actions import LxcProvider

providers_class_map = {
    lxc.provider_name: LxcProvider
}

