#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

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
                print("当前无流量数据，请使用流量片刻再来查看统计!")
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


if __name__ == '__main__':

    RESTART_CMD = "service v2ray restart"

    FIND_V2RAY_CRONTAB_CMD = "crontab -l|grep v2ray"

    DEL_UPDATE_TIMER_CMD = "crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt && crontab crontab.txt >/dev/null 2>&1 && rm -f crontab.txt >/dev/null 2>&1"

    while True:
        loader = Loader()

        profile = loader.profile

        group_list = profile.group_list

        print("当前流量统计状态: {}".format(profile.stats.status))

        print("")
        print("1.开启流量统计\n")
        print("2.关闭流量统计\n")
        print("3.查看流量统计\n")
        print("4.重置流量统计\n")
        print("tip: 具有有效email节点才会统计, 重启v2ray会重置流量统计!!!\n")

        choice = input("请输入数字选择功能：")
        if choice == "1":
            if os.popen(FIND_V2RAY_CRONTAB_CMD).readlines():
                rchoice = input("开启流量统计会关闭定时更新v2ray服务, 是否继续y/n: ")
                if rchoice == "y" or rchoice == "Y":
                    #关闭定时更新v2ray服务
                    os.system(DEL_UPDATE_TIMER_CMD)
                else:
                    print("撤销开启流量统计!!")
                    continue
            gw = GlobalWriter(group_list)
            gw.write_stats(True)
            os.system(RESTART_CMD)
            print("开启流量统计成功!\n")
            
        elif choice == "2":
            gw = GlobalWriter(group_list)
            gw.write_stats(False)
            os.system(RESTART_CMD)
            print("关闭流量统计成功!\n")
        elif choice == "3" or choice == "4":
            is_reset = (False if choice == "3" else True)
            action_info = ("查看" if choice == "3" else "重置")
            if not profile.stats.status:
                print("流量统计开启状态才能{}统计\n".format(action_info))
                continue
            
            if group_list[-1].node_list[-1].user_number > 1:
                print(profile)
                schoice = input("请输入所需要{}流量的组别(字母)或者序号(数字): ".format(action_info))
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
                                    print("无有效邮箱，无法统计!!!\n")
                                find = True
                                break
            elif schoice.isalpha() and schoice <= group_list[-1].tag:
                sf.get_stats(schoice, is_reset, True)
                sf.print_stats()
            else:
                print("输入有误! 请重新输入\n")
        else:
            break