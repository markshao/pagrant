#!/usr/bin/python
#coding:utf8

__author__ = 'markshao'

from pagrant.basecommand import Command


class InitCommand(Command):
    name = "init"
    usage = """%prog """
    summary = "help init the environment for the test"

    def __init__(self):
        pass