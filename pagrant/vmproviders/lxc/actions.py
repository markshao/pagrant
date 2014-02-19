#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

import time
from pagrant.vmproviders import BaseProvider
from pagrant.vendors import lxclite as lxc
from pagrant.exceptions import VirtualBootstrapError, PagrantError
from pagrant.util import write_json_fd, read_dict_fd

IP_COMMAND_0 = "awk '{ print $4,$3 }' /var/lib/misc/dnsmasq.leases | column -t | grep %s |awk '{print $2}'"

IP_COMMAND_1 = "lxc-ls --fancy|grep %s|awk '{print $3}'"  # lxc version: 1.0.0.alpha1


class LxcProvider(BaseProvider):
    def __init__(self, provider_info, logger):
        super(LxcProvider, self).__init__(provider_info, logger)

    def create_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.create(machine_setting['name'], template=machine_setting['template'],
                          guest_ip=machine_setting["ip"]) == 0:
                self.logger.info("create the machine <%s> successfully" % machine_setting['name'])
            else:
                # self.logger.error("Fail to create the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to create the vm [%s] " % machine_setting['name'])

    def start_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.start(machine_setting['name']) == 0:
                self.logger.warn("start the vm <%s> successfully" % machine_setting['name'])
                time.sleep(10)  # Launchpad 1264338
            else:
                # self.logger.error("Fail to start the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to start the vm [%s] " % machine_setting['name'])

    def stop_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.stop(machine_setting['name']) == 0:
                self.logger.info("stop the vm <%s> successfully" % machine_setting['name'])
            else:
                # self.logger.error("Fail to stop the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to stop the vm [%s] " % machine_setting['name'])

    def destroy_machines(self, machine_settings):
        for machine_name, machine_setting in machine_settings.items():
            if lxc.destroy(machine_setting['name']) == 0:
                self.logger.warn("destroy the vm <%s> successfully" % machine_setting['name'])
            else:
                # self.logger.error("Fail to destroy the vm [%s]" % machine_setting['name'])
                raise VirtualBootstrapError("Fail to destroy the vm [%s] " % machine_setting['name'])

    def get_machine_ip(self, machine_setting):
        from commands import getstatusoutput, getoutput  # solve the loop problem

        version = getoutput("lxc-version|awk '{print $3}'")

        if version.startswith("1.0"):
            results = getstatusoutput(IP_COMMAND_1 % machine_setting["name"])
        else:
            results = getstatusoutput(IP_COMMAND_0 % machine_setting["name"])

        if not results[0] == 0:
            raise PagrantError("Could not get the ip")

        return results[1]

    def persistent_to_local(self, machine_settings, path):
        res = {}
        for machine_name, machine_setting in machine_settings.items():
            res[machine_name] = machine_setting['name']
        write_json_fd(res, path)

    def clean_from_persistent(self, path):
        res = read_dict_fd(path)
        for key, value in res.items():
            lxc.stop(value)
        for key, value in res.items():
            lxc.destroy(value)