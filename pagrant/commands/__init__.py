#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from pagrant.commands.vmp import VmpCommand
from pagrant.commands.init import InitCommand
from pagrant.commands.test import TestCommand

commands = {
    VmpCommand.name: VmpCommand,
    InitCommand.name: InitCommand,
    TestCommand.name: TestCommand
}


def get_summaries(ignore_hidden=True, ordered=True):
    """Yields sorted (command name, command summary) tuples."""

    cmditems = commands.items()

    for name, command_class in cmditems:
        if ignore_hidden and command_class.hidden:
            continue
        yield (name, command_class.summary)


def get_similar_commands(name):
    """Command name auto-correct."""
    from difflib import get_close_matches

    close_commands = get_close_matches(name, commands.keys())

    if close_commands:
        guess = close_commands[0]
    else:
        guess = False

    return guess
