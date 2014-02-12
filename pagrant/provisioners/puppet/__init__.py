__author__ = 'root'

import os
from pagrant.exceptions import PagrantError
from pagrant.provisioners import BaseProvisioner


class PuppetProvisioner(BaseProvisioner):
    def __init__(self, machine, logger, provision_info, provider_info):
        super(PuppetProvisioner, self).__init__(machine, logger, provision_info, provider_info)

    def check_puppet(self):
        command = "which puppet"
        result = self.machine.execute_command(command)
        if result[1] != 0:
            self.logger.warn("The puppet is not installed on the machine <%s>" % self.machine.machine_info['name'])
            raise PagrantError("The puppet is not installed on <%s>" % self.machine.machine_info['name'])

    def check_manifest_file(self):
        manifest_name = self.provision_info.get("manifest", None)
        if not manifest_name:
            return False

        manifest_path = "manifests" + os.path.sep + manifest_name
        if not os.path.exists(manifest_path):
            raise PagrantError("The manifest file %s not exists " % manifest_path)

        return os.path.abspath(manifest_path)

    def do_provision(self):
        self.check_puppet()
        manifest_path_local = self.check_manifest_file()
        self.upload_puppet_file(manifest_path_local)
        self.call_puppet()

    def upload_puppet_file(self, manifest_path_local):
        manifest_name = self.provision_info.get("manifest", None)
        manifest_path_remote = "/tmp/%s" % manifest_name
        if self.machine.path_exists(manifest_path_remote):
            self.logger.warn("The puppet file existed") # fix me
            result, result_code = self.machine.delete_file_by_path(manifest_path_remote)
            if result_code != 0:
                raise PagrantError("Could not delete the file %s" % manifest_path_remote)

        self.machine.upload_dir_to_remote(manifest_path_local, "/tmp/")

    def call_puppet(self):
        manifest_name = self.provision_info.get("manifest", None)
        manifest_path_remote = "/tmp/%s" % manifest_name

        result, result_code = self.machine.execute_command("puppet apply %s" % manifest_path_remote)
        if result_code != 0:
            self.logger.error("could not provision for the  machine <%s>" % self.machine.machine_info['name'])
            raise PuppetProvisioner("could not provision for the  machine <%s>" % self.machine.machine_info['name'])

    def install_puppet(self):
        result = self.machine.sudo_execute_command("apt-get update")
        if result[1] != 0:
            self.logger.error("could not install the puppet for the machine <%s>" % self.machine.machine_info['name'])
            raise PagrantError("Fail to install the puppet")

        result = self.machine.sudo_execute_command("apt-get install -y puppet")
        if result[1] != 0:
            self.logger.error("could not install the puppet for the machine <%s>" % self.machine.machine_info['name'])
