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

    def create_machine(self, machine_setting):
        NotImplemented

    def start_machine(self, machine_setting):
        NotImplemented

    def stop_machine(self, machine_setting):
        NotImplemented

    def destroy_machine(self, machine_setting):
        NotImplemented


from pagrant.vmproviders.lxc.actions import LxcProvider

providers_class_map = {
    lxc.provider_name: LxcProvider
}

