#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.basecommand import Command


class TestCommand(Command):
    name = "test"
    usage = """%prog [options] """
    summary = "execute the test suites|cases with the options"
