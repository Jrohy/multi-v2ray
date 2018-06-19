#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import os
import re
from base_util import v2ray_util
from base_util import tool_box

RESTART_CMD = "service v2ray restart"

mul_user_conf = read_json.multiUserConf

while True:
    print("当前流量统计状态: %s" % read_json.conf_stats)

    print("")
    print("1.开启流量统计")
    print("2.关闭流量统计")
    print("3.查看流量统计")
    print("tip: 有效邮箱地址节点才会统计")

    choice = input("请输入数字选择功能：")
    if choice == "1":
        write_json.write_stats("on", mul_user_conf)
        os.system(RESTART_CMD)
        print("开启流量统计成功!")
    elif choice == "2":
        write_json.write_stats("off", mul_user_conf)
        os.system(RESTART_CMD)
        print("关闭流量统计成功!")
    elif choice == "3":
        if read_json.conf_stats == "关闭":
            print("流量统计开启状态才能查看统计")
            continue
        import server_info
        length = len(mul_user_conf)

        choice = input("请输入所需要查看流量的组别(字母)或者序号(数字)")

        if len(choice) == 1:
            door_port = read_json.conf_door_port
            choice=choice.upper()
            if tool_box.is_number(choice) and (choice > 0 and choice <= length):
                email = mul_user_conf[choice]["email"]
                if email == "":
                    print("无有效邮箱，无法统计!!!")
                    continue                    
                v2ray_util.get_stats(0, email, door_port)
            elif re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']:
                v2ray_util.get_stats(1, choice, door_port)
            else:
                print("输入有误!请检查是否在范围内")
        else:
            print("输入有误!")
    else:
        break