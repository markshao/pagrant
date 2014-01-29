__author__ = 'root'

from pagrant.exceptions import PagrantError
from pagrant.provisioners import BaseProvisioner


class PuppetProvisioner(BaseProvisioner):
    def __init__(self, machine, logger, provider_info):
        super(PuppetProvisioner, self).__init__(machine, logger, provider_info)

    def check_puppet(self):
        command = "which puppet"
        result = self.machine.execute_command(command)
        if result[1] != 0:
            self.logger.warn("The puppet is not installed on the machine <%s>" % self.machine.machine_info['name'])

    def install_puppet(self):
        result = self.machine.sudo_execute_command("apt-get update")
        if result[1] != 0:
            self.logger.error("could not install the puppet for the machine <%s>" % self.machine.machine_info['name'])
            raise PagrantError("Fail to install the puppet")

        result = self.machine.sudo_execute_command("apt-get isntall -y puppet")
        if result[1] != 0:
            self.logger.error("could not install the puppet for the machine <%s>" % self.machine.machine_info['name'])
