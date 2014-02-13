__author__ = 'markshao'

import string
from pagrant.exceptions import PagrantError


class BaseProvisioner(object):
    def __init__(self, machine, logger, provision_info, provider_info=None):
        self.machine = machine
        self.logger = logger
        self.provider_info = provider_info
        self.provision_info = provision_info

    def provision(self):
        self.do_provision()


from pagrant.provisioners.puppet import PuppetProvisioner
from pagrant.provisioners.web.tomcat import TomcatProvisioner
from pagrant.provisioners.health.http import HttpCheckerPrivisioner

provision_map = {
    "puppet": PuppetProvisioner,
    "tomcat": TomcatProvisioner,
    "http_health": HttpCheckerPrivisioner
}


# used by the machine
def provision_machine(machine, provision_list, logger, vmprovider_info):
    global provision_map

    logger.info("provision the vm <%s>" % machine.machine_info["name"])
    for provision in provision_list:
        provision_type = provision.get("type", None)
        if not provision_type:
            raise PagrantError("The provision type is not spcified")
        provision_type = string.lower(provision_type)

        if provision_type not in provision_map:
            raise PagrantError("The provision type %s is not support by pagrant" % provision_type)

        provision_instance = provision_map[provision_type](machine, logger, provision, vmprovider_info)
        provision_instance.provision()
