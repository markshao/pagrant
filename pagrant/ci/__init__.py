__author__ = 'root'

import base64
import subprocess
import time

import os
from pagrant.exceptions import PagrantError


CONNECTIONS = 10
TIMEOUT = 5 * 60


def get_axel_path():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'downloader', 'axel')


class CIBuild(object):
    def __init__(self, logger, ci_config):
        self.logger = logger
        self.ci_config = ci_config

    def get_latest_artifact_url(self):
        NotImplemented

    def download_to_local(self, destination, need_authentication=False):
        if os.path.exists(destination):
            os.remove(destination)

        if need_authentication:
            b64Val = base64.b64encode("%s:%s" % (self.username, self.password))
            authentication_header = "Authorization: Basic %s" % b64Val
            download_command = [get_axel_path(), "-n", str(CONNECTIONS), "-H", "'%s'" % authentication_header, "-o",
                                destination, self.get_latest_artifact_url()]

        else:
            download_command = [get_axel_path(), "-n", str(CONNECTIONS), "-o",
                                destination, self.get_latest_artifact_url()]

        print download_command
        start_download_time = time.time()
        try:
            download_process = subprocess.Popen(download_command)
        except Exception, e:
            raise PagrantError("could not start the download proecess")

        while ((time.time() - start_download_time) <= TIMEOUT):
            status = download_process.poll()
            if not status and status != 0:
                time.sleep(5)
                continue
            if status != 0:
                raise PagrantError("download fail")
            else:
                break
        else:
            raise PagrantError("Timeout")

        if not os.path.exists(destination):
            raise PagrantError("download fail")