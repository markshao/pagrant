#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.commands.vmp import VmpCommand

commands = {
    VmpCommand.name: VmpCommand
}


def get_summaries(ignore_hidden=True, ordered=True):
    """Yields sorted (command name, command summary) tuples."""

    cmditems = commands.items()

    for name, command_class in cmditems:
        if ignore_hidden and command_class.hidden:
            continue
        yield (name, command_class.summary)
