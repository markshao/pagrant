__author__ = 'markshao'


class BaseProvisioner(object):
    def __init__(self, machine, logger, provider_info=None):
        self.machine = machine
        self.logger = logger
        self.provider_info = provider_info

