#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']


class PagrantError(Exception):
    """The base exception for the pagrant"""
    pass


class CommandError(PagrantError):
    """ Command parser error """
    pass
