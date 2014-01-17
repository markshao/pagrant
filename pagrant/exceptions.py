#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']


class PagrantError(Exception):
    """The base exception for the pagrant"""
    pass


class CommandError(PagrantError):
    """ Command parser error """
    pass


class PagrantConfigError(PagrantError):
    """ The pagrantConfig file error
    """
    pass


class VirtualBootstrapError(PagrantError):
    """
        The virtual boostrap error
    """
    pass


class VmProviderError(PagrantError):
    """
        The virtual boostrap error
    """
    pass


class TestError(PagrantError):
    """
        Nose Test Error
    """
    pass
