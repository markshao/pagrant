__author__ = 'root'

from pagrant.ci import CIBuild
from tc import TeamCityRESTApiClient


class TeamCityBuild(CIBuild):
    def __init__(self, logger, ci_config):
        super(TeamCityBuild, logger).__init__()
        self.tc_host = ci_config.get("host", None)
        assert self.tc_host
        self.tc_port = ci_config.get("port", None)

        self.username = ci_config.get("username", None)
        self.password = ci_config.get("password", None)

        self.tc = TeamCityRESTApiClient(self.username, self.password, self.tc_host, self.tc_port)

        self.project_name = ci_config.get("project_name", None)