#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import commands
import time
from pagrant.vmproviders import BaseProvider
from pagrant.vendors import lxclite as lxc
from pagrant.exceptions import VirtualBootstrapError, PagrantError

IP_COMMAND_0 = "awk '{ print $4,$3 }' /var/lib/misc/dnsmasq.leases | column -t | grep %s |awk '{print $2}'"

IP_COMMAND_1 = "lxc-ls --fancy|grep %s|awk '{print $3}'"  # lxc version: 1.0.0.alpha1


class LxcProvider(BaseProvider):
    name = "lxc"

    def create_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.create(machine_setting['name'], template=machine_setting['template'],
                          guest_ip=machine_setting["ip"]) == 0:
                self.logger.warn("Finish create the machine [%s]" % machine_setting['name'])
            else:
                self.logger.error("Fail to create the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to create the vm [%s] " % machine_setting['name'])

    def start_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.start(machine_setting['name']) == 0:
                self.logger.warn("Successfully start the vm [%s]" % machine_setting['name'])
                time.sleep(10)  # Launchpad 1264338
            else:
                self.logger.error("Fail to start the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to start the vm [%s] " % machine_setting['name'])


    def stop_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.stop(machine_setting['name']) == 0:
                self.logger.warn("Successfully stop the vm [%s]" % machine_setting['name'])
            else:
                self.logger.error("Fail to stop the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to stop the vm [%s] " % machine_setting['name'])


    def destroy_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.destroy(machine_setting['name']) == 0:
                self.logger.warn("Successfully destroy the vm [%s]" % machine_setting['name'])
            else:
                self.logger.error("Fail to destroy the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to destroy the vm [%s] " % machine_setting['name'])


    def get_machine_ip(self, machine_setting):
        version = commands.getoutput("lxc-version|awk '{print $3}'")

        if version.startswith("1.0"):
            results = commands.getstatusoutput(IP_COMMAND_1 % machine_setting["name"])
        else:
            results = commands.getstatusoutput(IP_COMMAND_0 % machine_setting["name"])

        if not results[0] == 0:
            raise PagrantError("Could not get the ip")

        return results[1]