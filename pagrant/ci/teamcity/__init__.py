__author__ = 'root'

from pagrant.ci import CIBuild
from tc import TeamCityRESTApiClient
from pagrant.exceptions import PagrantError


class TeamCityBuild(CIBuild):
    def __init__(self, logger, ci_config):
        super(TeamCityBuild, self).__init__(logger, ci_config)
        self.tc_host = self.ci_config.get("host", None)
        assert self.tc_host
        self.tc_port = self.ci_config.get("port", None)

        self.username = self.ci_config.get("username", None)
        self.password = self.ci_config.get("password", None)

        self.tc = TeamCityRESTApiClient(self.username, self.password, self.tc_host, self.tc_port)

        self.build_type_name = self.ci_config.get("build_type_name", None)
        self.artifact_name = self.ci_config.get("artifact_name", None)

    def project_id_by_name(self, project_name):
        self.tc.get_all_projects()
        for project in self.tc.get_from_server()["project"]:
            if project["name"] == project_name:
                return project["id"]
        raise PagrantError("The project is not found")

    def get_build_type_id_by_name(self, build_type_name):
        self.tc.get_all_build_types()
        for build_type in self.tc.get_from_server()['buildType']:
            if build_type['name'] == build_type_name:
                return build_type['id']
        raise PagrantError("The build type is not found")

    def get_latest_build_id(self, build_type_id):
        self.tc.get_all_builds_by_build_type_id(build_type_id)
        return self.tc.get_from_server()['build'][0]['id']

    def get_latest_artifact_url(self):
        build_type_id = self.get_build_type_id_by_name(self.build_type_name)
        latest_build_id = self.get_latest_build_id(build_type_id)
        return "http://%s:%s/repository/download/%s/%s:id/%s" % (
            self.tc_host, self.tc_port, build_type_id, latest_build_id, self.artifact_name)


if __name__ == "__main__":
    tcb = TeamCityBuild(None, {
        "host": "shdssinttc1.dctmlabs.com",
        "port": 6080,
        "username": "shaom2",
        "password": ")Slamdunk1986",
        "build_type_name": "xCPRestServices_Main_Standalone",
        "artifact_name": "xcp-rest.war"
    })

    print tcb.download_to_local("/home/mark/Downloads/xcp-rest.war", True)