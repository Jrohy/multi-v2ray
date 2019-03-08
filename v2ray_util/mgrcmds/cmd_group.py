#!/usr/bin/env python3
# coding: utf-8

from . import cmdopt
from . import cmdutil
from ..util_core.v2ray import V2ray
from ..config_modify import multiple


def doit(argstr):
    cmdutil.run_std_sub_command(subcmd, argstr)

def cmd_user_add(cmds, uconf, params):
    multiple.new_user()
    V2ray.restart()

def cmd_user_del(cmds, uconf, params):
    multiple.del_user()
    V2ray.restart()

def cmd_port_add(cmds, uconf, params):
    multiple.new_port()
    V2ray.restart()

def cmd_port_del(cmds, uconf, params):
    multiple.del_port()
    V2ray.restart()


groupParser = cmdopt.build_parser(
        usage = 'Manager Group: add or delete user and port.'
        )

subcmd = {
    'user': {
        'add': cmdutil.Command(groupParser, cmd_user_add),
        'del': cmdutil.Command(groupParser, cmd_user_del),
    },
    'port': {
        'add': cmdutil.Command(groupParser, cmd_port_add),
        'del': cmdutil.Command(groupParser, cmd_port_del),
    },
}
