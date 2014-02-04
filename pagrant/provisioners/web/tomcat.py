#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.provisioners import BaseProvisioner


class TomcatProvisioner(BaseProvisioner):
    def __init__(self, machine, logger, provision_info, provider_info):
        super(TomcatProvisioner, self).__init__(machine, logger, provision_info, provider_info)

    def check_tomcat_installed(self):
        pass