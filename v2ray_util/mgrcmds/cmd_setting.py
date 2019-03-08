#!/usr/bin/env python3
# coding: utf-8

import subprocess
import pkg_resources

from . import cmdopt
from . import cmdutil
from ..util_core import client
from ..util_core.v2ray import V2ray
from ..config_modify import multiple
from ..global_setting import stats_ctr, iptables_ctr, ban_bt


def doit(argstr):
    cmdutil.run_std_sub_command(subcmd, argstr)

def cmd_traffic_v2ray(cmds, uconf, params):
    stats_ctr.manage()

def cmd_traffic_iptables(cmds, uconf, params):
    iptables_ctr.manage()

def cmd_ban_bt(cmds, uconf, params):
    ban_bt.manage()
    V2ray.restart()

def cmd_schedule_update(cmds, uconf, params):
    subprocess.call("bash {0}".format(pkg_resources.resource_filename(__name__, "global_setting/update_timer.sh")), shell=True)

def cmd_clean_log(cmds, uconf, params):
    V2ray.cleanLog()

def cmd_generate_client_config(cmds, uconf, params):
    client.generate()

settingParser = cmdopt.build_parser(
        usage = ('Global Setting:\n'
            '    V2ray Traffic Statistics\n'
            '    Iptables Traffic Statistics\n'
            '    Ban Bittorrent\n'
            '    Schedule Update V2ray\n'
            '    Clean Log\n'
            '    Generate Client Config'
            )
        )

subcmd = {
    'traffic_v2ray':    cmdutil.Command(settingParser, cmd_traffic_v2ray),
    'traffic_iptables': cmdutil.Command(settingParser, cmd_traffic_iptables),
    'ban_bt':           cmdutil.Command(settingParser, cmd_ban_bt),
    'schedule_update':  cmdutil.Command(settingParser, cmd_schedule_update),
    'clean_log':        cmdutil.Command(settingParser, cmd_clean_log),

    'generate_client_config': cmdutil.Command(settingParser, cmd_generate_client_config),
}
