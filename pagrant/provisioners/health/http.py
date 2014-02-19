__author__ = ['Xiaobo']

import time
import httplib
from pagrant.exceptions import VirtualBootstrapError
from pagrant.provisioners import BaseProvisioner

CHECK_TIMEOUT = 60 * 5


class HttpCheckerPrivisioner(BaseProvisioner):
    def __init__(self, machine, logger, provision_info, provider_info):
        super(HttpCheckerPrivisioner, self).__init__(machine, logger, provision_info, provider_info)
        self.port = self.provision_info.get("port", None)
        self.url = self.provision_info.get("url", None)

    def do_provision(self):
        self.check_health()

    def check_health(self):
        time.sleep(5)
        start_time = time.time()
        self.logger.start_progress("start to check the %s for application to be ready" % self.machine.machine_info['name'])
        while True:
            self.logger.info("Wait for the application to be ready on the %s ..." % self.machine.machine_info['name'])
            con = httplib.HTTPConnection(self.machine.host, self.port)
            con.request("GET", self.url)
            res = con.getresponse()
            if res.status == 200 or res.status == 401:
                self.logger.info("The url %s could be accessed normally on the %s" % (self.url, self.machine.machine_info['name']))
                self.logger.end_progress()
                break
            else:
                duration = time.time() - start_time
                if duration > CHECK_TIMEOUT:
                    raise VirtualBootstrapError("The url %s could not be accessed normally on the %s" % (self.url, self.machine.machine_info['name']))
                else:
                    time.sleep(5)
                    continue
