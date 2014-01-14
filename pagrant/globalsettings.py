#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import os

PROJECT_NAME = "pagrant"

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))[:-len(PROJECT_NAME)]

PAGRANT_SRC_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

PAGRANT_CONFIG_TEMPLATE_PATH = os.path.join(PAGRANT_SRC_ROOT_PATH, "templates", "Pagrantfile.py")

# vmprovider

VMPROVIDER_LIST_DICT = ".vmprovider_dict"