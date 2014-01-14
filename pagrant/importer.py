#!/usr/bin/python
#coding:utf8

__author__ = ['Xiaobo']

import sys
import imp


def import_module_ext(path):
    index = path.rfind('/')
    module_name = path[index + 1:]
    module_path = path[:index]
    return import_module(module_name, module_path)


def import_module(module_name, module_path):
    f, path, desc = imp.find_module(module_name, sys.path.append(module_path))

    try:
        return imp.load_module(module_name, f, path, desc)
    finally:
        if f:
            f.close()