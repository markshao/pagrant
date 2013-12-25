#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

STATUS = {
    'RUNNING': 1,
    'STOP': 0
}


class Machine(object):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
