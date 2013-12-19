#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys
from pagrant.commands import commands
from pagrant.cmdparser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pagrant.exceptions import PagrantError
from pagrant.util import get_prog
from pagrant import cmdoptions


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

    parser.main = True # so the help formatter knows

    return parser


def parse_opts(args):
    main_parser = create_main_parser()

    # first get the general options
    general_options, args_else = main_parser.parse_args(args)

    if not args_else or (args_else[0] == 'help' and len(args_else) == 1):
        main_parser.print_help()
        sys.exit()

    # the subcommand name
    cmd_name = args_else[0].lower()

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
    except PagrantError:
        e = sys.exc_info()[1]
        sys.stderr.write("ERROR: %s" % e)
        sys.stderr.write(os.linesep)
        sys.exit(1)

    command = commands[cmd_name]()
    command.execute(cmd_args)

