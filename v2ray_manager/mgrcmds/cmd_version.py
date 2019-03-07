#!/usr/bin/env python3
# coding: utf-8

import cmdutil
import opt
import v2ray_util
from pykit import proc
from pykit import strutil


def doit(argstr):
    cmdutil.run_std_sub_command(subcmd, argstr)

def cmd_show(cmds, uconf, params):

    _, out, _ = proc.command_ex('/usr/bin/v2ray/v2ray', '-version')
    v2ray_v = out.split('\n')[0].split()[1]

    cmdutil.message('      v2ray: {v}'.format(v=
                        strutil.green(v2ray_v)))
    cmdutil.message('multi V2ray: {v}'.format(v=
                        strutil.green(v2ray_util.__version__)))

showParser = opt.build_parser(
        usage = 'show v2ray and v2ray_util version.'
        )

subcmd = {
    '__shortcut__': 'show',
    'show': cmdutil.Command(showParser, cmd_show),
}
