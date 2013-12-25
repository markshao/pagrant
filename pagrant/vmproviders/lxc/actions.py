#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

from pagrant.vmproviders import BaseProvider
from pagrant.vendors import lxclite as lxc
from pagrant.exceptions import VirtualBootstrapError


class LxcProvider(BaseProvider):
    name = "lxc"

    def create_machine(self, machine_setting):
        if lxc.create(machine, template=machine_setting['template']) == 0:
            self.logger.warn("Finish create the machine [%s]" % machine)
        else:
            raise VirtualBootstrapError("Fail to create the vm [%s] " % machine)


