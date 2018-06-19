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

is_first = True

while True:
    #不是第一次读取json则需要重新读取
    if not is_first:
        from importlib import reload
        reload(read_json)
    print("当前流量统计状态: %s" % read_json.conf_stats)

    print("")
    print("1.开启流量统计\n")
    print("2.关闭流量统计\n")
    print("3.查看流量统计\n")
    print("tip: 有效邮箱地址节点才会统计\n")

    choice = input("请输入数字选择功能：")
    if choice == "1":
        write_json.write_stats("on", mul_user_conf)
        os.system(RESTART_CMD)
        print("开启流量统计成功!\n")
    elif choice == "2":
        write_json.write_stats("off", mul_user_conf)
        os.system(RESTART_CMD)
        print("关闭流量统计成功!\n")
    elif choice == "3":
        if read_json.conf_stats == "关闭":
            print("流量统计开启状态才能查看统计\n")
            continue
        os.system("python3 /usr/local/v2ray.fun/server_info.py")
        length = len(mul_user_conf)

        choice = input("请输入所需要查看流量的组别(字母)或者序号(数字)")

        if len(choice) == 1:
            door_port = read_json.conf_door_port
            choice=choice.upper()
            if tool_box.is_number(choice) :
                choice = int(choice)
                if choice > 0 and choice <= length:
                    email = mul_user_conf[choice - 1]["email"]
                    if email == "":
                        print("无有效邮箱，无法统计!!!\n")
                    else:                   
                        v2ray_util.get_stats(0, email, door_port)
                    continue
            elif re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']:
                v2ray_util.get_stats(1, choice, door_port)
                continue
            print("输入有误! 请检查是否在范围内\n")
        else:
            print("输入有误!\n")  
    else:
        break

    is_first = False