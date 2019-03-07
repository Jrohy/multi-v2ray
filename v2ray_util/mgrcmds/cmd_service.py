#!/usr/bin/env python3
# coding: utf-8

from . import cmdopt
from . import cmdutil
from ..pykit import proc
from ..pykit import strutil


def doit(argstr):
    cmdutil.run_std_sub_command(subcmd, argstr)

def cmd_service(cmds, uconf, params):

    act = cmds[-1]

    _, out, _ = proc.command_ex('/usr/sbin/service', 'v2ray', act)
    cmdutil.message(out)
    cmdutil.message('')
    cmdutil.message('service v2ray {act}, success.'.format(act=
                        strutil.green(act)))

subcmd = {
    '__shortcut__': 'status',
    'start':    cmdutil.Command(cmdopt.emptyParser, cmd_service),
    'stop':     cmdutil.Command(cmdopt.emptyParser, cmd_service),
    'restart':  cmdutil.Command(cmdopt.emptyParser, cmd_service),
    'status':   cmdutil.Command(cmdopt.emptyParser, cmd_service),
}
