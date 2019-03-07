#!/usr/bin/env python2
# coding: utf-8

from . import cmdopt
from . import cmdutil
from ..pykit import strutil


def colorstr( s, clr ):
    return str( strutil.ColoredString( s, clr ) )

def doit( argstr ):
    cmdutil.run_std_sub_command( subcmd, argstr )

def cmd_lscolor( cmds, uconf, params ):

    cmdutil.message( ''.join([ colorstr( str(b).ljust(4), b ) for b in range(16) ]) )

    for x in range(6):
        cmdutil.message( ''.join([ colorstr( str(x*36+b+16).ljust(4), x*36+b+16 ) for b in range(36) ]) )

    cmdutil.message( ''.join([ colorstr( str(b).ljust(4), b ) for b in range(232,256) ]) )

subcmd = {
    'lscolor': cmdutil.Command(cmdopt.emptyParser, cmd_lscolor),
}
