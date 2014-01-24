#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

import sys
import traceback

import os


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

TRUE_BOOLEAN = ("YES", "Y")
FALSE_BOOLEAN = ("NO", "N")


def get_prog():
    return 'pagrant'


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


def get_userinput(msg, retry=3):
    for i in xrange(retry):
        resp = raw_input(msg)
        if resp.upper() in TRUE_BOOLEAN + FALSE_BOOLEAN:
            break
    else:
        sys.stderr.write("The pagrant could been created due to the user's wrong input\n")
        sys.exit(1)
    return resp


def is_true(value):
    return value.upper() in TRUE_BOOLEAN


def format_exc(exc_info=None):
    if exc_info is None:
        exc_info = sys.exc_info()
    out = StringIO()
    traceback.print_exception(*exc_info, **dict(file=out))
    return out.getvalue()


try:
    from cPickle import load, dump
except ImportError:
    from pickle import load, dump


def write_json_fd(dist, fpath):
    if os.path.exists(fpath):
        os.remove(fpath)
    f = open(fpath, "wb")
    dump(dist, f)
    f.close()


def read_dict_fd(fpath):
    f = open(fpath, "rb")
    obj = load(f)
    f.close()
    return obj