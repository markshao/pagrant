#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import copy
import time

import paramiko
from pagrant.pagrantfile import ContextConfig
from pagrant.exceptions import VirtualBootstrapError
from pagrant.vmproviders import providers_class_map
from pagrant.machine import Machine
from pagrant.test import test_context
from pagrant.importer import import_module


# each test contains a environment for test

SSH_TIMEOUT = 60 * 5


class Environment(object):
    def __init__(self, pagrantfile_path, logger):
        self.pagrantfile_path = pagrantfile_path
        self.context_config = ContextConfig(self.pagrantfile_path)

        self.logger = logger

        # decide the vmprovider to user
        vmprovider = self.context_config.get_vmprovider()

        if vmprovider.get("type") == "local":
            vmprovider_path = vmprovider.get("path")
            vmprovider_name = vmprovider.get("name")
            vmprovider_init = import_module(vmprovider_name, vmprovider_path)
            vmprovider_action = import_module(vmprovider_init.provider_action_module,
                                              vmprovider_path + "/" + vmprovider_name)
            vmprovider_class = vmprovider_action.LxcProvider
        else:
            vmprovider_class = providers_class_map.get(vmprovider.get("type"))

        self.vmprovider_config = self.context_config.get_vmprovider_config()

        self._vmprovider = vmprovider_class(self.context_config.get_vmprovider_config(), self.logger)
        self.machines_info = copy.deepcopy(self.context_config.get_machine_settings())
        self.machines = None  # store all the machines

    @property
    def vmprovider(self):
        return self._vmprovider

    def create_machines(self):
        self._vmprovider.create_machines(self.machines_info)

    def start_machines(self):
        self._vmprovider.start_machines(self.machines_info)

    def stop_machines(self):
        self._vmprovider.stop_machines(self.machines_info)

    def destroy_machines(self):
        self._vmprovider.destroy_machines(self.machines_info)

    def init_test_context(self):
        machines = {}
        for machine_name in self.machines_info.keys():
            machine = self.machines_info[machine_name]
            machine_ip = machine.get("ip", None)
            if not machine_ip:
                machine["ip"] = self._vmprovider.get_machine_ip(machine)
                if not machine["ip"] or len(machine["ip"]) == 0:
                    raise VirtualBootstrapError("could not get the ip")
                self.logger.warn("The machine %s ip is [%s] " % (machine_name, machine["ip"]))

            _m = Machine(machine["ip"], self.vmprovider_config["username"], self.vmprovider_config["password"])
            machines[machine_name] = _m

        # init the test context
        test_context.set_machines(machines)

        # set the machines to the environment
        self.machines = machines

    def check_machine_ssh(self):
        self.logger.warn("check the ssh accessible for the machines")
        for machine_name, machine in self.machines.items():
            start_time = time.time()
            self.logger.start_progress("start check the %s for ssh ready" % machine_name)
            while True:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(machine.host, 22, machine.username, machine.password, timeout=20)
                    self.logger.end_progress()
                    break   #if no error throwed
                except Exception, e:
                    duration = time.time() - start_time
                    if duration > SSH_TIMEOUT:
                        self.logger.end_progress()
                        raise VirtualBootstrapError("The machine %s could not been normally startup" % machine_name)
                    else:
                        self.logger.show_progress("wait %s seconds for the %s to ready" % (duration, machine_name))
                        time.sleep(5)
                        continue
