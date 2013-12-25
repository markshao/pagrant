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


class Machine(object):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
