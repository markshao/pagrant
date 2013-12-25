#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import commands
from pagrant.vmproviders import BaseProvider
from pagrant.vendors import lxclite as lxc
from pagrant.exceptions import VirtualBootstrapError, PagrantError

IP_COMMAND = "awk '{ print $4,$3 }' /var/lib/misc/dnsmasq.leases | column -t | grep %s |awk '{print $2}'"


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

    def get_machine_ip(self, machine_setting):
        result = commands.getstatusoutput(IP_COMMAND % machine_setting['name'])
        if not result[0] == 0:
            raise PagrantError("execute the ip command fail")
        else:
            return result[1]