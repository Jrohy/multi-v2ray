#!/usr/bin/env python3
# coding: utf-8

import cmdutil
import opt
from pykit import proc
from pykit import strutil


def doit(argstr):
    cmdutil.run_std_sub_command(subcmd, argstr)

def cmd_service(cmds, uconf, params):

    act = cmds[-1]

    proc.command_ex('service v2ray {act}'.format(act=act))
    cmdutil.message('v2ray {act} success.'.format(act=
                        strutil.green(act)))

subcmd = {
    '__shortcut__': 'status',
    'start':    cmdutil.Command(opt.emptyParser, cmd_service),
    'stop':     cmdutil.Command(opt.emptyParser, cmd_service),
    'restart':  cmdutil.Command(opt.emptyParser, cmd_service),
    'status':   cmdutil.Command(opt.emptyParser, cmd_service),
}
