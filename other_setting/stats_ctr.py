#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import os
import re
from base_util import v2ray_util
from base_util import tool_box

RESTART_CMD = "service v2ray restart"

FIND_V2RAY_CRONTAB_CMD = "crontab -l|grep v2ray"

DEL_UPDATE_TIMER_CMD = "crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt && crontab crontab.txt >/dev/null 2>&1 && rm -f crontab.txt >/dev/null 2>&1"

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

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
        write_json.write_stats("on", mul_user_conf)
        os.system(RESTART_CMD)
        print("开启流量统计成功!\n")
        
    elif choice == "2":
        write_json.write_stats("off", mul_user_conf)
        os.system(RESTART_CMD)
        print("关闭流量统计成功!\n")
    elif choice == "3" or choice == "4":
        is_reset = (False if choice == "3" else True)
        action_info = ("查看" if choice == "3" else "重置")
        if read_json.conf_stats == "关闭":
            print("流量统计开启状态才能%s统计\n" % action_info)
            continue
        
        if length > 1:
            os.system("python3 /usr/local/v2ray.fun/server_info.py")

            schoice = input("请输入所需要%s流量的组别(字母)或者序号(数字)" % action_info)
        else:
            schoice = "A"

        if len(schoice) == 1:
            door_port = read_json.conf_door_port
            schoice=schoice.upper()
            if tool_box.is_number(schoice) :
                schoice = int(schoice)
                if schoice > 0 and schoice <= length:
                    email = mul_user_conf[schoice - 1]["email"]
                    if email == "":
                        print("无有效邮箱，无法统计!!!\n")
                    else:                   
                        v2ray_util.get_stats(0, email, door_port, is_reset)
                    continue
            elif re.match(r'[A-Z]', schoice) and schoice <= mul_user_conf[-1]['indexDict']['group']:
                v2ray_util.get_stats(1, schoice, door_port, is_reset)
                continue
            print("输入有误! 请检查是否在范围内\n")
        else:
            print("输入有误!\n")  
    else:
        break

    is_first = False