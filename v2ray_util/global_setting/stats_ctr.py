#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import subprocess

from v2ray_util import run_type
from ..util_core.v2ray import V2ray
from ..util_core.loader import Loader
from ..util_core.writer import GlobalWriter
from ..util_core.utils import bytes_2_human_readable, ColorStr, readchar

class StatsFactory:
    def __init__(self, door_port):
        self.door_port = door_port
        self.downlink_value = 0
        self.uplink_value = 0

    def __run_command(self, command):
        value = 0
        result = bytes.decode(subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip())
        result_list = re.findall(r"\s+\d+\s+", result)
        if "v2ctl" not in result and len(result_list) == 1:
            value = int(result_list[0])
        return value

    def get_stats(self, meta_info, is_reset=False, is_group=False):
        is_reset = "true" if is_reset else "false"
        type_tag = ("inbound" if is_group else "user")

        if run_type == "xray":
            stats_cmd = "cd /usr/bin/xray && ./xray api stats --server=127.0.0.1:{} -name \"{}>>>{}>>>traffic>>>{}\""
            if is_reset == "true":
                stats_cmd = stats_cmd + " -reset"
        else:
            stats_cmd = "cd /usr/bin/v2ray && ./v2ctl api --server=127.0.0.1:{} StatsService.GetStats 'name: \"{}>>>{}>>>traffic>>>{}\"" + " reset: {}'".format(is_reset)

        stats_real_cmd = stats_cmd.format(str(self.door_port), type_tag, meta_info, "downlink")
        self.downlink_value = self.__run_command(stats_real_cmd)

        stats_real_cmd = stats_cmd.format(str(self.door_port), type_tag, meta_info, "uplink")
        self.uplink_value = self.__run_command(stats_real_cmd)

    def print_stats(self, horizontal=False):
        if horizontal:
            print("downlink: {0} uplink: {1} total: {2}".format(
                ColorStr.cyan(bytes_2_human_readable(self.downlink_value, 2)),
                ColorStr.cyan(bytes_2_human_readable(self.uplink_value, 2)),
                ColorStr.cyan(bytes_2_human_readable(self.downlink_value + self.uplink_value, 2)))
            )
        else:
            print('''
downlink: {0}  
uplink: {1} 
total: {2}
            '''.format(ColorStr.cyan(bytes_2_human_readable(self.downlink_value, 2)),
            ColorStr.cyan(bytes_2_human_readable(self.uplink_value, 2)),
            ColorStr.cyan(bytes_2_human_readable(self.downlink_value + self.uplink_value, 2)))
            )

def manage():

    FIND_V2RAY_CRONTAB_CMD = "crontab -l|grep {}".format(run_type)

    DEL_UPDATE_TIMER_CMD = "crontab -l|sed '/SHELL=/d;/{}/d' > crontab.txt && crontab crontab.txt >/dev/null 2>&1 && rm -f crontab.txt >/dev/null 2>&1".format(run_type)

    while True:
        loader = Loader()

        profile = loader.profile

        group_list = profile.group_list

        print("{}: {}".format(_("{} Traffic Statistics Status".format(run_type.capitalize())), profile.stats.status))

        print("")
        print(_("1.open statistics"))
        print("")
        print(_("2.close statistics"))
        print("")
        print(_("3.check user statistics result"))
        print("")
        print(_("4.check group statistics result"))
        print("")
        print(_("5.reset statistics"))
        print("")
        print(_("tip: restart {} will reset traffic statistics!!!".format(run_type)))
        print("")

        choice = readchar(_("please select: "))

        if choice in ("3", "4", "5") and not profile.stats.status:
            print(_("only open traffic statistics to operate"))
            print("")
            continue

        if choice == "1":
            if os.popen(FIND_V2RAY_CRONTAB_CMD).readlines():
                rchoice = readchar(_("open traffic statistics will close schedule update {}, continue?(y/n): ".format(run_type)))
                if rchoice == "y" or rchoice == "Y":
                    #关闭定时更新v2ray服务
                    os.system(DEL_UPDATE_TIMER_CMD)
                else:
                    print(_("undo open traffic statistics!!"))
                    continue
            gw = GlobalWriter(group_list)
            gw.write_stats(True)
            V2ray.restart()
            print(_("open traffic statistics success!"))
            print("")
            
        elif choice == "2":
            gw = GlobalWriter(group_list)
            gw.write_stats(False)
            V2ray.restart()
            print(_("close traffic statistics success!"))
            print("")

        elif choice == "3":
            sf = StatsFactory(profile.stats.door_port)
            print("")
            for group in group_list:
                port_way = "-{}".format(group.end_port) if group.end_port else ""
                for node in group.node_list:
                    print('''
Group: {group.tag}
IP: {color_ip}
Port: {group.port}{port_way}
{node}             
                    '''.format(group=group, color_ip=ColorStr.fuchsia(group.ip), node=node, port_way=port_way).strip())
                    if node.user_info:
                        sf.get_stats(node.user_info, False)
                        sf.print_stats(horizontal=True)
                    else:
                        print(ColorStr.yellow(_("no effective email!!!")))
                    print("")

        elif choice == "4":
            sf = StatsFactory(profile.stats.door_port)
            print("")
            for group in group_list:
                tls = _("open") if group.tls == "tls" else _("close")
                port_way = "-{}".format(group.end_port) if group.end_port else ""
                print('''
Group: {group.tag}
IP: {color_ip}
Port: {group.port}{port_way}
TLS: {tls}
                '''.format(group=group, color_ip=ColorStr.fuchsia(group.ip), tls=tls, port_way=port_way).strip())
                sf.get_stats(group.tag, False, True)
                sf.print_stats(horizontal=True)
                print("")

        elif choice == "5":
            if group_list[-1].node_list[-1].user_number > 1:
                print(profile)
                schoice = input(_("please input number or group alphabet to reset: "))
            else:
                schoice = "A"

            sf = StatsFactory(profile.stats.door_port)
            schoice=schoice.upper()
            if schoice.isnumeric() :
                schoice = int(schoice)
                if schoice > 0 and schoice <= group_list[-1].node_list[-1].user_number:
                    find = False
                    for group in group_list:
                        if find:
                            break
                        for node in group.node_list:
                            if node.user_number == schoice:
                                if node.user_info:
                                   sf.get_stats(node.user_info, True)
                                   sf.print_stats()
                                else:
                                    print(_("no effective email!!!"))
                                    print("")
                                find = True
                                break
            elif schoice.isalpha() and schoice <= group_list[-1].tag:
                sf.get_stats(schoice, True, True)
                sf.print_stats()
            else:
                print(_("input error, please input again"))
                print("")
        else:
            break