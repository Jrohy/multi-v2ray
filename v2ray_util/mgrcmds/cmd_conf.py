#!/usr/bin/env python3
# coding: utf-8

from . import cmdopt
from . import cmdutil
from ..util_core.v2ray import V2ray
from ..util_core.utils import open_port
from ..config_modify import base, ss, stream, tls


def doit(argstr):
    cmdutil.run_std_sub_command(subcmd, argstr)

def cmd_conf(cmds, uconf, params):
    act = cmds[-1]
    act_func[act]()
    V2ray.restart()

def cmd_conf_info(cmds, uconf, params):
    V2ray.info()

def _act_port():
    base.port()
    open_port()


act_func = {
    'email': base.new_email,
    'uuid': base.new_uuid,
    'alter_id': base.alterid,
    'port': _act_port,
    'stream': stream.modify,
    'tls': tls.modify,
    'tcp_fast_open': base.tfo,
    'dyn_port': base.dyn_port,
    'ss_method': lambda : ss.modify('method'),
    'ss_password': lambda : ss.modify('password'),
}

confParser = cmdopt.build_parser(
        usage = 'Modify Config: [{acts}]'.format(
            acts='|'.join(list(act_func.keys())))
        )

subcmd = {
    'info': cmdutil.Command(cmdopt.emptyParser, cmd_conf_info)
}
for k in act_func:
    subcmd[k] = cmdutil.Command(confParser, cmd_conf)
