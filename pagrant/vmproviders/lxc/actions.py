#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

from pagrant.vmproviders import BaseProvider
from pagrant.vendors import lxclite as lxc


class LxcProvider(BaseProvider):
    name = "lxc"

    def _create_machines(self, machine_settings):
        for machine in machine_settings.keys():
            if lxc.create(machine, template=machine_settings[machine]['template']) == 0:
                self.logger.warn("Finish create the machine %s \n" % machine)
