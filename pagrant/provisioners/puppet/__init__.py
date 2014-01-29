__author__ = 'root'


class Provisioner(object):
    def __init__(self, machine, logger, provider_info):
        self.machine = machine
        self.logger = logger
        self.provider_info = provider_info

    def check_puppet(self):
        command = "which puppet"
        result = self.machine.execute_command(command)
        if result[1] != 0:
            self.logger.warn("The puppet is not installed on the machine <%s>" % self.machine.machine_info['name'])

    def install_puppet(self):
        pass
