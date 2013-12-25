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

    def create_machine(self, machine_setting):
        NotImplemented

    def create_machines(self, machines_setting):
        try:
            for machine in machines_setting.keys():
                self.create_machine(machines_setting[machine])
        except Exception, e:
            raise VirtualBootstrapError(str(e))

    def start_machine(self, machine_setting):
        pass

    def start_machines(self, machines_setting):
        try:
            for machine in machines_setting.keys():
                self.start_machine(machines_setting[machine])
        except Exception, e:
            raise VirtualBootstrapError(str(e))

    def stop_machine(self, machine_setting):
        pass

    def stop_machines(self, machines_setting):
        try:
            for machine in machines_setting.keys():
                self.stop_machine(machines_setting[machine])
        except Exception, e:
            raise VirtualBootstrapError(str(e))

    def destroy_machine(self, machine_setting):
        pass

    def destroy_machiens(self, machines_setting):
        try:
            for machine in machines_setting.keys():
                self.destroy_machien(machines_setting[machine])
        except Exception, e:
            raise VirtualBootstrapError(str(e))


from pagrant.vmproviders.lxc.actions import LxcProvider

providers_class_map = {
    lxc.provider_name: LxcProvider
}

