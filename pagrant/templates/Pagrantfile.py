#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

# pagrant version
PAGRANT_VERSION = "1.0"

# the provider for the usage
vmprovider = "lxc"


def vmprovider_config():
    return {
        "name": "lxc",
        "username": "ubuntu",
        "password": "password"
    }


def machine_settings():
    machines = {}

    # example for define the machine_a example
    machines['test-server'] = {
        "ip": "10.0.3.7",
        "template": "ubuntu",
        "name": "test-server"
    }

    return machines
