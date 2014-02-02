__author__ = 'root'

from pagrant.ci import CIBuild
from tc import TeamCityRESTApiClient
from pagrant.exceptions import PagrantError


class TeamCityBuild(CIBuild):
    def __init__(self, logger, ci_config):
        super(TeamCityBuild, self).__init__(logger)
        self.tc_host = ci_config.get("host", None)
        assert self.tc_host
        self.tc_port = ci_config.get("port", None)

        self.username = ci_config.get("username", None)
        self.password = ci_config.get("password", None)

        self.tc = TeamCityRESTApiClient(self.username, self.password, self.tc_host, self.tc_port)

        self.project_name = ci_config.get("project_name", None)

    def project_id_by_name(self, name):
        self.tc.get_all_projects()
        for project in self.tc.get_from_server()["project"]:
            if project["name"] == name:
                return project["id"]
        raise PagrantError("The project is not found")


if __name__ == "__main__":
    tcb = TeamCityBuild(None, {
        "host": "shdssinttc1.dctmlabs.com",
        "port": 6080,
        "username": "shaom2",
        "password": ")Slamdunk1986"
    })

    print tcb.project_id_by_name("Documentum REST Services")
