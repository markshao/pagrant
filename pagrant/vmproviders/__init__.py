#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.vmproviders import lxc

providers = {
    lxc.provider_name: lxc.privider_summary,
}


class BaseProvider(object):
    pass