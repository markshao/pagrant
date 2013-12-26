#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']


class TestContext(object):
    def __init__(self):
        self.machines = {}

    def set_machines(self, machines):
        self.machines = machines


test_context = TestContext()