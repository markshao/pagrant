#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys
from cmdparser import parse_opts
from exceptions import PagrantError


def pagrant_main(init_args=None):
    if init_args is None:
        init_args == sys.argv[1:]

    try:
        cmd_name, cmd_args = parse_opts(init_args)
    except PagrantError:
        e = sys.exc_info()[1]
        sys.stderr.write("ERROR: %s" % e)
        sys.stderr.write(os.linesep)
        sys.exit(1)