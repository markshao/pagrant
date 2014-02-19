#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.vmproviders import lxc
from pagrant.vmproviders import docker


providers = {
    lxc.provider_name: lxc.privider_summary,
    docker.provider_name: docker.privider_summary
}


class BaseProvider(object):
    def __init__(self, provider_info, logger):
        self.logger = logger
        self.provider_info = provider_info

    def create_machines(self, machine_settings):
        NotImplemented

    def start_machines(self, machine_settings):
        NotImplemented

    def stop_machines(self, machine_settings):
        NotImplemented

    def destroy_machines(self, machine_settings):
        NotImplemented

    def get_machine_ip(self, machine_setting):
        NotImplemented

    def persistent_to_local(self, machine_settings, path):
        NotImplemented

    def clean_from_persistent(self, path):
        NotImplemented


from pagrant.vmproviders.lxc.actions import LxcProvider
from pagrant.vmproviders.docker.actions import DockerProvider

providers_class_map = {
    lxc.provider_name: LxcProvider,
    docker.provider_name: DockerProvider
}

