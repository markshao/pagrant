#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

from pagrant.vmproviders import BaseProvider
from pagrant.vendors.docker import Client
from pagrant.util import write_json_fd, read_dict_fd


class DockerProvider(BaseProvider):
    def __init__(self, provider_info, logger):
        super(DockerProvider, self).__init__(provider_info, logger)
        self.docker_client = Client()
        self.container_map = {}
        self.default_image = provider_info['default_image']
        self.command = "/usr/sbin/sshd -D"  # FIX ME

    def create_machines(self, machine_settings):
        for machine_name, machine in machine_settings.items():
            image = machine.get("image", None)
            image = image if image else self.default_image
            volumes = machine.get("volumes", None)
            __dns = machine.get("dns", None)
            res = self.docker_client.create_container(image=image, command=self.command, detach=True,
                                                      volumes=volumes.values(), dns=__dns)
            self.container_map[machine_name] = res['Id']
            self.logger.info("create the container <%s> successfully" % machine_name)

    def start_machines(self, machine_settings):
        for machine_name, machine in machine_settings.items():
            volumes = machine['volumes']
            self.docker_client.start(self.container_map[machine_name], binds=volumes)
            self.logger.info("start the container <%s> successfully " % machine_name)

    def stop_machines(self, machine_settings):
        for machine_name, machine in machine_settings.items():
            self.docker_client.stop(self.container_map[machine_name])
            self.logger.info("stop the container <%s> successfully " % machine_name)

    def destroy_machines(self, machine_settings):
        for machine_name, machine in machine_settings.items():
            self.docker_client.remove_container(self.container_map[machine_name])
            self.logger.info("delete the container <%s> successfully " % machine_name)

    def get_machine_ip(self, machine_setting):
        container_id = self.container_map[machine_setting['name']]
        container_info = self.docker_client.inspect_container(container_id)
        return container_info['NetworkSettings']['IPAddress']

    def persistent_to_local(self, machine_settings, path):
        write_json_fd(self.container_map, path)


    def clean_from_persistent(self, path):
        res = read_dict_fd(path)

        for key, value in res.items():
            self.docker_client.stop(value)

        for key, value in res.items():
            self.docker_client.remove_container(value)