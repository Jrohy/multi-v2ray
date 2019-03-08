#!/usr/bin/env python3
# coding: utf-8

from . import cmdopt
from . import cmdutil
from ..util_core.v2ray import V2ray


def doit(argstr):
    cmdutil.run_std_sub_command(subcmd, argstr)

def cmd_service(cmds, uconf, params):
    act = cmds[-1]
    getattr(V2ray, act)()

def cmd_update_v2ray(cmds, uconf, params):
    V2ray.update()

def cmd_renew_v2ray(cmds, uconf, params):
    V2ray.new()


subcmd = {
    '__shortcut__': 'status',
    'start':    cmdutil.Command(cmdopt.emptyParser, cmd_service),
    'stop':     cmdutil.Command(cmdopt.emptyParser, cmd_service),
    'restart':  cmdutil.Command(cmdopt.emptyParser, cmd_service),
    'status':   cmdutil.Command(cmdopt.emptyParser, cmd_service),
    'update':   cmdutil.Command(cmdopt.emptyParser, cmd_update_v2ray),
    'renew':    cmdutil.Command(cmdopt.emptyParser, cmd_renew_v2ray),
}
