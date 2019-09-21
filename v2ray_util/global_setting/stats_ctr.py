#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

from ..util_core.v2ray import V2ray
from ..util_core.loader import Loader
from ..util_core.writer import GlobalWriter
from ..util_core.utils import bytes_2_human_readable, ColorStr

class StatsFactory:
    def __init__(self, door_port):
        self.door_port = door_port
        self.downlink_value = 0
        self.uplink_value = 0

    def get_stats(self, meta_info, is_reset=False, is_group=False):
        is_reset = "true" if is_reset else "false"

        stats_cmd = "cd /usr/bin/v2ray && ./v2ctl api --server=127.0.0.1:%s StatsService.GetStats 'name: \"%s>>>%s>>>traffic>>>%s\" reset: %s'"
        type_tag = ("inbound" if is_group else "user")

        stats_real_cmd = stats_cmd % (str(self.door_port), type_tag, meta_info, "downlink", is_reset)
        downlink_result = os.popen(stats_real_cmd).readlines()
        if downlink_result and len(downlink_result) == 5:
            re_result = re.findall(r"\d+", downlink_result[2])
            if not re_result:
                print(_("no data traffic now!"))
                return
            self.downlink_value = int(re_result[0])

        stats_real_cmd = stats_cmd % (str(self.door_port), type_tag, meta_info, "uplink", is_reset)
        uplink_result = os.popen(stats_real_cmd).readlines()
        if uplink_result and len(uplink_result) == 5:
            re_result = re.findall(r"\d+", uplink_result[2])
            self.uplink_value = int(re_result[0])

    def print_stats(self):
        print('''
downlink: {0}  
uplink: {1} 
total: {2}
        '''.format(ColorStr.cyan(bytes_2_human_readable(self.downlink_value, 2)),
        ColorStr.cyan(bytes_2_human_readable(self.uplink_value, 2)),
        ColorStr.cyan(bytes_2_human_readable(self.downlink_value + self.uplink_value, 2)))
        )

def manage():

    FIND_V2RAY_CRONTAB_CMD = "crontab -l|grep v2ray"

    DEL_UPDATE_TIMER_CMD = "crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt && crontab crontab.txt >/dev/null 2>&1 && rm -f crontab.txt >/dev/null 2>&1"

    while True:
        loader = Loader()

        profile = loader.profile

        group_list = profile.group_list

        print("{}: {}".format(_("V2ray Traffic Statistics Status"), profile.stats.status))

        print("")
        print(_("1.open statistics"))
        print("")
        print(_("2.close statistics"))
        print("")
        print(_("3.check statistics result"))
        print("")
        print(_("4.reset statistics"))
        print("")
        print(_("tip: only have email node can statistics, restart v2ray will reset traffic statistics!!!"))
        print("")

        choice = input(_("please select: "))
        if choice == "1":
            if os.popen(FIND_V2RAY_CRONTAB_CMD).readlines():
                rchoice = input(_("open traffic statistics will close schedule update v2ray, continue?(y/n): "))
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

        elif choice == "3" or choice == "4":
            is_reset = (False if choice == "3" else True)
            action_info = ("check" if choice == "3" else "reset")
            if not profile.stats.status:
                print("{} {}".format(_("only open traffic statistics can"), action_info))
                print("")
                continue
            
            if group_list[-1].node_list[-1].user_number > 1:
                print(profile)
                schoice = input("{} {}: ".format(_("please input number or group alphabet to"), action_info))
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
                        for index, node in enumerate(group.node_list):
                            if node.user_number == schoice:
                                if node.user_info:
                                   sf.get_stats(node.user_info, is_reset)
                                   sf.print_stats()
                                else:
                                    print(_("no effective email!!!"))
                                    print("")
                                find = True
                                break
            elif schoice.isalpha() and schoice <= group_list[-1].tag:
                sf.get_stats(schoice, is_reset, True)
                sf.print_stats()
            else:
                print(_("input error, please input again"))
                print("")
        else:
            break