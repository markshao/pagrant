#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

from pagrant.vmproviders import BaseProvider
from pagrant.vendors import lxclite as lxc
from pagrant.exceptions import VirtualBootstrapError


class LxcProvider(BaseProvider):
    name = "lxc"

    def create_machine(self, machine_setting):
        if lxc.create(machine_setting['name'], template=machine_setting['template']) == 0:
            self.logger.warn("Finish create the machine [%s]" % machine_setting['name'])
        else:
            self.logger.error("Fail to create the vm [%s]" % machine_setting['name'])
            raise VirtualBootstrapError("Fail to create the vm [%s] " % machine_setting['name'])

    def start_machine(self, machine_setting):
        if lxc.start(machine_setting['name']) == 0:
            self.logger.warn("Successfully start the vm [%s]" % machine_setting['name'])
        else:
            self.logger.error("Fail to start the vm [%s]" % machine_setting['name'])
            raise VirtualBootstrapError("Fail to start the vm [%s] " % machine_setting['name'])

    def stop_machine(self, machine_setting):
        if lxc.stop(machine_setting['name']) == 0:
            self.logger.warn("Successfully stop the vm [%s]" % machine_setting['name'])
        else:
            self.logger.error("Fail to stop the vm [%s]" % machine_setting['name'])
            raise VirtualBootstrapError("Fail to stop the vm [%s] " % machine_setting['name'])

    def destroy(self, machine_setting):
        if lxc.destroy(machine_setting['name']) == 0:
            self.logger.warn("Successfully destroy the vm [%s]" % machine_setting['name'])
        else:
            self.logger.error("Fail to destroy the vm [%s]" % machine_setting['name'])
            raise VirtualBootstrapError("Fail to destroy the vm [%s] " % machine_setting['name'])