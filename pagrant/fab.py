#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from fabric.api import settings
from fabric.operations import run, put, hide, sudo
from fabric.contrib import files


class FabricSupport(object):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def execute_shell_command(self, command, pty=None):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), host_string=self.host, user=self.username,
                      password=self.password, warn_only=True):
            if not pty:
                result = run(command, shell=True)
            else:
                result = run(command, shell=True, pty=False)

            return result, result.return_code

    def sudo_execute_shell_command(self, command):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), host_string=self.host, user=self.username,
                      password=self.password, warn_only=True):
            result = sudo(command, user=self.username)
            return result, result.return_code

    def upload_directory(self, local_dir, remote_dir):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), host_string=self.host, user=self.username,
                      password=self.password, warn_only=True):
            if not files.exists(remote_dir):
                self.execute_shell_command("mkdir %s" % remote_dir)  # FIX ME ,just support the 1 layer dir
            put(local_dir, remote_dir)

    def path_existed(self, path):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), host_string=self.host, user=self.username,
                      password=self.password, warn_only=True):
            return files.exists(path)

    def get_environment(self, environment_name):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), host_string=self.host, user=self.username,
                      password=self.password, warn_only=True):
            command = "echo $%s" % environment_name
            result = run(command, shell=True)
            if result.return_code == 0:
                return result
            else:
                return None