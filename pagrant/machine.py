#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

STATUS = {
    'NEW_CREATED': 0,
    'RUNNING': 1,
    'STOP': 2,
    'DESTROY': 3,
    'UNKNOWN': -99
}

from pagrant.fab import FabricSupport


class Machine(object):
    def __init__(self, host, username, password, machine_info):
        self.host = host
        self.username = username
        self.password = password
        self.group_id = machine_info['group_id']
        self.type = machine_info['type']
        self.machine_info = machine_info

        self._fabric = FabricSupport(self.host, self.username, self.password)

    def execute_command(self, command, pty=None):
        return self._fabric.execute_shell_command(command, pty)

    def sudo_execute_command(self, command):
        return self._fabric.sudo_execute_shell_command(command)

    def upload_dir_to_remote(self, local_dir, remote_dir):
        self._fabric.upload_directory(local_dir, remote_dir)

    def path_exists(self, path):
        return self._fabric.path_existed(path)

    def delete_file_by_path(self, path):
        return self._fabric.execute_shell_command("rm -f %s" % path)

    def get_env(self, env_name):
        return self._fabric.get_environment(env_name)

