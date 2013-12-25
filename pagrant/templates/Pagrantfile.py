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
        "template": "ubuntu"
    }


def machine_settings():
    machines = {}

    # example for define the machine_a example
    machines['test-server'].ip = None
    machines['test-server'].template = 'ubuntu'
    machines['test-server'].name = 'test-server'

    return machines
