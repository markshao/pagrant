#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import copy
from pagrant.pagrantfile import ContextConfig
from pagrant.exceptions import VirtualBootstrapError
from pagrant.vmproviders import providers_class_map
from pagrant.machine import STATUS, Machine
from pagrant.test import test_context
from pagrant.importer import import_module_ext
from pagrant.importer import import_module

# each test contains a environment for test


class Environment(object):
    def __init__(self, pagrantfile_path, logger):
        self.pagrantfile_path = pagrantfile_path
        self.context_config = ContextConfig(self.pagrantfile_path)

        self.logger = logger

        # decide the vmprovider to user
        vmprovider_type = self.context_config.get_vmprovider_type()
        
        if vmprovider_type == "local":
            vmprovider_path = self.context_config.get_vmprovider_path()
            vmprovider_init = import_module_ext(vmprovider_path)
            vmprovider_action = import_module(vmprovider_init.provider_action_module, vmprovider_path)
            vmprovider_class = vmprovider_action.LxcProvider
        else:
            vmprovider_class = providers_class_map.get(vmprovider_type)

        self.vmprovider_config = self.context_config.get_vmprovider_config()

        self._vmprovider = vmprovider_class(self.context_config.get_vmprovider_config(), self.logger)
        self.machines_info = copy.deepcopy(self.context_config.get_machine_settings())

    @property
    def vmprovider(self):
        return self._vmprovider

    def create_machines(self):
        for machine_name in self.machines_info.keys():
            machine = self.machines_info[machine_name]
            machine_state = getattr(machine, "status", STATUS['UNKNOWN'])
            if not machine_state == STATUS['UNKNOWN']:
                raise VirtualBootstrapError(
                    "The vm [%s] is not in the right status,current status is [%s],should be unknown" % machine,
                    machine_state)

            self._vmprovider.create_machine(machine)
            machine["status"] = STATUS['NEW_CREATED']

    def start_machines(self):
        for machine_name in self.machines_info.keys():
            machine = self.machines_info[machine_name]
            machine_state = machine.get("status", STATUS['UNKNOWN'])
            if machine_state == STATUS['RUNNING']:
                self.logger.warn("The vm [%s] is already in the running mode" % machine_name)

            if machine_state in (STATUS['STOP'], STATUS['NEW_CREATED']):
                self._vmprovider.start_machine(machine)
                machine["status"] = STATUS['RUNNING']
            else:
                raise VirtualBootstrapError("the vm [%s] is not in the right status" % machine_name)

    def stop_machines(self):
        for machine_name in self.machines_info.keys():
            machine = self.machines_info[machine_name]
            machine_state = machine.get("status", STATUS['UNKNOWN'])
            if machine_state == STATUS['STOP']:
                self.logger.warn("The vm [%s] is already in the stop mode" % machine_name)

            if machine_state in (STATUS['RUNNING'],):
                self._vmprovider.stop_machine(machine)
                machine["status"] = STATUS['STOP']
            else:
                raise VirtualBootstrapError("the vm [%s] is not in the right status" % machine_name)

    def destroy_machines(self):
        for machine_name in self.machines_info.keys():
            machine = self.machines_info[machine_name]
            machine_state = machine.get("status", STATUS['UNKNOWN'])
            if machine_state == STATUS['DESTROY']:
                self.logger.warn("The vm [%s] is already in the running mode" % machine_name)

            if machine_state in (STATUS['STOP'], STATUS['NEW_CREATED']):
                self._vmprovider.destroy_machine(machine)
                machine["status"] = STATUS['DESTROY']
            else:
                raise VirtualBootstrapError("the vm [%s] is not in the right status" % machine_name)

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
