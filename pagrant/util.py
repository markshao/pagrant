#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys
import os

def get_prog():
    try:
        if os.path.basename(sys.argv[0]) in ('__main__.py', '-c'):
            return "%s -m pip" % sys.executable
    except (AttributeError, TypeError, IndexError):
        pass
    return 'pip'


def get_terminal_size():
    """Returns a tuple (x, y) representing the width(x) and the height(x)
    in characters of the terminal window."""

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct

            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return None
        if cr == (0, 0):
            return None
        if cr == (0, 0):
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (os.environ.get('LINES', 25), os.environ.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])