#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import copy
from pagrant.vendors.myoptparser.optparse import OptionGroup, SUPPRESS_HELP, Option


def make_option_group(group, parser):
    """
    Return an OptionGroup object
    group  -- assumed to be dict with 'name' and 'options' keys
    parser -- an optparse Parser
    """
    option_group = OptionGroup(parser, group['name'])
    for option in group['options']:
        option_group.add_option(option.make())
    return option_group


class OptionMaker(object):
    """Class that stores the args/kwargs that would be used to make an Option,
    for making them later, and uses deepcopy's to reset state."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def make(self):
        args_copy = copy.deepcopy(self.args)
        kwargs_copy = copy.deepcopy(self.kwargs)
        return Option(*args_copy, **kwargs_copy)

###########
# options #
###########

help_ = OptionMaker(
    '-h', '--help',
    dest='help',
    action='help',
    help='Show help.')

version = OptionMaker(
    '-V', '--version',
    dest='version',
    action='store_true',
    help='Show version and exit.')

quiet = OptionMaker(
    '-q', '--quiet',
    dest='quiet',
    action='count',
    default=0,
    help='Give less output.')

log = OptionMaker(
    '--log',
    dest='log',
    metavar='path',
    help='Path to a verbose appending log. This log is inactive by default.')

log_explicit_levels = OptionMaker(
    # Writes the log levels explicitely to the log'
    '--log-explicit-levels',
    dest='log_explicit_levels',
    action='store_true',
    default=False,
    help=SUPPRESS_HELP)

log_file = OptionMaker(
    # The default log file
    '--log-file', '--local-log',
    dest='log_file',
    metavar='path',
    default='~/pagrant.log', # may need change later
    help='Path to a verbose non-appending log, that only logs failures. This log is active by default at %default.')

general_group = {
    'name': 'General Options',
    'options': [
        help_,
        version
        #log,
        #log_explicit_levels,
        #log_file
    ]
}

only_help_group = {
    'name': 'General Options',
    'options': [
        help_,
    ]
}