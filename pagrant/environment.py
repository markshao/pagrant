#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import copy
import time

import paramiko
from pkg_resources import load_entry_point
from pagrant.pagrantfile import ContextConfig
from pagrant.exceptions import VirtualBootstrapError, PagrantConfigError
from pagrant.vmproviders import providers_class_map
from pagrant.machine import Machine
from pagrant.test import test_context
from pagrant.importer import import_module
from pagrant.commands.vmp import get_installed_vmproviders
from pagrant.provisioners import provision_machine


# each test contains a environment for test

SSH_TIMEOUT = 60 * 5


class Environment(object):
    def __init__(self, pagrantfile_path, logger):
        self.pagrantfile_path = pagrantfile_path
        self.context_config = ContextConfig(self.pagrantfile_path)

        self.logger = logger

        # decide the vmprovider to user
        self.vmprovider_info = self.context_config.get_vmprovider()
        self.vmprovider_type = self.vmprovider_info.get("type")

        if self.vmprovider_type == "local":
            vmprovider_path = self.vmprovider_info.get("path")
            vmprovider_name = self.vmprovider_info.get("name")
            vmprovider_init = import_module(vmprovider_name, vmprovider_path)
            vmprovider_action = import_module(vmprovider_init.provider_action_module,
                                              vmprovider_path + "/" + vmprovider_name)
            vmprovider_class = vmprovider_action.LxcProvider
        elif self.vmprovider_type in providers_class_map:
            vmprovider_class = providers_class_map.get(self.vmprovider_info.get("type"))
        elif self.vmprovider_type in get_installed_vmproviders():
            vmprovider_class = load_entry_point(self.vmprovider_info.get("type"), "PAGRANT", "VMPROVIDER")
        else:
            raise PagrantConfigError("The vmprovider is not support by the system")

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

    def persistent_to_path(self, path):
        self._vmprovider.persistent_to_local(self.machines_info, path)

    def clean_from_persistent(self, path):
        self._vmprovider.clean_from_persistent(path)

    def init_test_context(self):
        machines = {}
        for machine_name in self.machines_info.keys():
            machine = self.machines_info[machine_name]
            machine_ip = machine.get("ip", None)
            if not machine_ip:
                machine["ip"] = self._vmprovider.get_machine_ip(machine)
                if not machine["ip"] or len(machine["ip"]) == 0:
                    raise VirtualBootstrapError("could not get the ip")
                self.logger.warn("vm <%s> IP is [%s] " % (machine_name, machine["ip"]))

            _m = Machine(machine["ip"], self.vmprovider_config["ssh_username"], self.vmprovider_config["ssh_password"],
                         machine)
            machines[machine_name] = _m

        # init the test context
        test_context.set_machines(machines)

        # set the machines to the environment
        self.machines = machines

    def check_machine_ssh(self):
        self.logger.warn("check the os ready with ssh ")
        for machine_name, machine in self.machines.items():
            start_time = time.time()
            self.logger.start_progress("start check the %s for ssh ready" % machine_name)
            while True:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    self.logger.show_progress("Wait for <%s> to be ready ..." % machine_name)
                    ssh.connect(machine.host, 22, machine.username, machine.password, timeout=20)
                    self.logger.end_progress()
                    break   # if no error throwed
                except Exception, e:
                    duration = time.time() - start_time
                    if duration > SSH_TIMEOUT:
                        self.logger.end_progress()
                        raise VirtualBootstrapError("The machine %s could not been normally startup" % machine_name)
                    else:
                        self.logger.show_progress("wait %s seconds for the %s to ready" % (duration, machine_name))
                        time.sleep(1)
                        continue

    def provision_environment(self):
        provision_machines = []
        for machine_name, machine_info in self.machines_info.items():
            provision_list = machine_info.get("provisions", None)
            if not provision_list or len(provision_list) == 0:
                self.logger.warn("machine <%s> does not need provision" % machine_name)
                continue
            else:
                provision_machines.append(self.machines[machine_name])

                # provision_machine(self.machines[machine_name], provision_list, self.logger, self.vmprovider_info)
        from pagrant.process import process_map

        process_map(provision_machines, provision_machine,
                    **dict(provision_list=provision_list, logger=self.logger, vmprovider_info=self.vmprovider_info))