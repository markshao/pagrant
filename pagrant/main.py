#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys
import os
from pagrant.commands import commands, get_summaries, get_similar_commands
from pagrant.cmdparser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pagrant.exceptions import PagrantError, CommandError
from pagrant.util import get_prog
from pagrant import cmdoptions
from pagrant.version import version_number
from pagrant.vendors.myoptparser.optparse import BadOptionError


def create_main_parser():
    parser_kw = {
        'usage': '\n%prog <command> [options]',
        'add_help_option': False,
        'formatter': UpdatingDefaultsHelpFormatter(),
        'name': 'global',
        'prog': get_prog(),
    }

    parser = ConfigOptionParser(**parser_kw)
    parser.disable_interspersed_args()

    # add the general options
    gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, parser)
    parser.add_option_group(gen_opts)

    # create command listing for description
    command_summaries = get_summaries()
    description = [''] + ['%-27s %s' % (i, j) for i, j in command_summaries]
    parser.description = '\n'.join(description)
    parser.main = True  # so the help formatter knows

    return parser


def parse_opts(args):
    main_parser = create_main_parser()

    # first get the general options
    general_options, args_else = main_parser.parse_args(args)

    if general_options.version:
        sys.stdout.write("version {}\n".format(version_number()))
        sys.exit()

    if not args_else or (args_else[0].lower() == 'help' and len(args_else) == 1):
        main_parser.print_help()
        sys.exit()

    # the subcommand name
    cmd_name = args_else[0].lower()

    # check the cmd_name existed
    if cmd_name not in commands:
        guess = get_similar_commands(cmd_name)
        msg = ['unknown command "%s"' % cmd_name]
        if guess:
            msg.append('maybe you meant "%s"' % guess)

        raise CommandError(' - '.join(msg))

    #all the args without the subcommand
    cmd_args = args[:]
    cmd_args.remove(args_else[0].lower())

    return cmd_name, cmd_args


def pagrant_main():
    """
        main function
    """

    args = sys.argv[1:]

    try:
        cmd_name, cmd_args = parse_opts(args)
    except BadOptionError, e:
        sys.stderr.write(str(e))
        sys.stderr.write(os.linesep)
        sys.exit(1)
    except PagrantError:
        e = sys.exc_info()[1]
        sys.stderr.write("ERROR: %s" % e)
        sys.stderr.write(os.linesep)
        sys.exit(1)

    command = commands[cmd_name]()
    command.execute(cmd_args)

