#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys

from pagrant.vendors.myoptparser import optparse
from pagrant import cmdoptions
from pagrant.cmdparser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pagrant.util import get_prog
from pagrant.exceptions import PagrantError, PagrantConfigError, VirtualBootstrapError
from pagrant.log import logger


__all__ = ['Command']


class Command(object):
    name = None
    usage = None
    hidden = None
    summary = ""

    def __init__(self):
        parser_kw = {
            'usage': self.usage,
            'prog': '%s %s' % (get_prog(), self.name),
            'formatter': UpdatingDefaultsHelpFormatter(),
            'add_help_option': False,
            'name': self.name,
            'description': self.__doc__,
        }

        self.parser = ConfigOptionParser(**parser_kw)

        # Commands should add options to this option group
        optgroup_name = '%s Options' % self.name.capitalize()
        self.cmd_opts = optparse.OptionGroup(self.parser, optgroup_name)

        # Add the general options
        gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, self.parser)
        self.parser.add_option_group(gen_opts)

        self.logger = None

        self.skip_parse = False

    def setup_logging(self):
        pass

    def parse_args(self, args):
        # factored out for testability
        return self.parser.parse_args(args)

    def run(self, args):
        """
            The sub command class should overide this method
        """
        NotImplemented

    def execute(self, args=None):
        """
            The main interface for exectute the command
        """

        import copy

        args_bk = copy.deepcopy(args)

        try:
            options = None
            if not self.skip_parse or len(args) == 0 or args[0] in ("-h", "--help"):
                options, args = self.parse_args(args)
        except (optparse.OptionError, optparse.BadOptionError), e:
            options = None

        level = logger.DEBUG  # Fix me to enable the user specify the log

        complete_log = []
        logger.add_consumers(
            (logger.VERBOSE_DEBUG, sys.stdout),
            (level, complete_log.append),
        )
        if getattr(options, "log_explicit_levels", False):
            logger.explicit_levels = True

        self.logger = logger  # if the sub command does nothing , we just reuse this log

        self.setup_logging()

        try:
            self.run(args_bk)
        except VirtualBootstrapError:
            self.logger.fatal("ERROR: %s" % str(sys.exc_info()[1]))
            # self.logger.error('Exception information:\n%s' % format_exc())
            sys.exit(1)
        except PagrantConfigError:
            self.logger.fatal("ERROR: %s" % str(sys.exc_info()[1]))
            # self.logger.error('Exception information:\n%s' % format_exc())
            sys.exit(1)
        except PagrantError:
            self.logger.fatal("ERROR: %s" % str(sys.exc_info()[1]))
            # self.logger.error('Exception information:\n%s' % format_exc())
            sys.exit(1)
        except KeyboardInterrupt:
            self.logger.fatal("The user interrupt the test case execution")
            sys.exit(1)
