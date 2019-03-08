#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import getopt
import sys

from .manager import Managecmd
from .util_core.v2ray import V2ray


def menu():

    V2ray.check()

    opts, argv = getopt.getopt(sys.argv[1:] , 'e:c:', ['nocolor',])
    opts = dict(opts)

    if '-e' in opts :
        dictate = opts['-e'].split(';') + ['exit']
    else :
        dictate = []

    mcmd = Managecmd(dictate)
    mcmd.cmdloop()

if __name__ == "__main__":
    menu()
