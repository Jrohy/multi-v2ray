#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from loader import Loader
from utils import color_str, Color, is_number, calcul_iptables_traffic

loader = Loader()

profile = loader.profile

group_list = profile.group_list

while True:
    print("Iptables 端口流量统计")
    print("")
    print("1.查看流量统计\n")
    print("2.重置流量统计\n")
    print("tip: 默认v2端口自动开启iptables的流量统计\n")

    choice = input("请输入数字选择功能：")
    if choice == "1":
        print("")
        for group in group_list:
            print(calcul_iptables_traffic(group.port))
        print("")

    elif choice == "2":
        port = input("请输入要重置流量的端口：")
        if port and is_number(port):
            os.system("bash /usr/local/multi-v2ray/global_setting/clean_traffic.sh {}".format(str(port)))
        else:
            print(color_str(Color.RED, "输入有误!"))
    else:
        break