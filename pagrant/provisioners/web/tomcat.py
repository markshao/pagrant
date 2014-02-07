#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.provisioners import BaseProvisioner
from pagrant.exceptions import PagrantError


class TomcatProvisioner(BaseProvisioner):
    def __init__(self, machine, logger, provision_info, provider_info):
        super(TomcatProvisioner, self).__init__(machine, logger, provision_info, provider_info)

    def check_tomcat_installed(self):
        # check the catalina_home in the provision info has been configured
        catalina_home = self.provider_info.get("catalina_home", None)
        if not catalina_home:
            catalina_home = self.machine.get_env("CATALINA_HOME")
            if not catalina_home:
                raise PagrantError("The catalina_home is not configured")

    def do_provision(self):
        self.check_tomcat_installed()