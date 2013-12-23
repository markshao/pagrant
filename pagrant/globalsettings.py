#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import os

PROJECT_NAME = "pagrant"

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))[:-len(PROJECT_NAME)]
TEMPLATE_PATH = os.path.join(ROOT_PATH, "templates")

PAGRANT_CONFIG_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, "Pagrantfile")