#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.test import test_context


def test_ls():
    machine = test_context.machines['test-server']
    print machine.execute_command("whoami")