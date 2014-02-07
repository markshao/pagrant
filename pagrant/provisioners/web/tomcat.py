#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import os
from pagrant.provisioners import BaseProvisioner
from pagrant.exceptions import PagrantError


class TomcatProvisioner(BaseProvisioner):
    def __init__(self, machine, logger, provision_info, provider_info):
        super(TomcatProvisioner, self).__init__(machine, logger, provision_info, provider_info)
        self.war = self.provision_info.get("war", None)
        assert self.war is not None

    def check_tomcat_installed(self):
        # check the catalina_home in the provision info has been configured
        self.catalina_home = self.provider_info.get("catalina_home", None)
        if not self.catalina_home:
            self.catalina_home = self.machine.get_env("CATALINA_HOME")
            if not self.catalina_home:
                raise PagrantError("The catalina_home is not configured")
        self.webapp_path = os.path.join(self.catalina_home, "webapps")

    def do_provision(self):
        self.check_tomcat_installed()
        self.deploy()

    def deploy(self):
        self.machine.upload_dir_to_remote(self.war, self.webapp_path)
        self.start_tomcat()

    def start_tomcat(self):
        start_sh = os.path.join(self.catalina_home, "bin", "startup.sh")
        result, code = self.machine.execute_command(start_sh, pty=True)
        self.logger.warn(result)
        self.logger.warn(str(code))