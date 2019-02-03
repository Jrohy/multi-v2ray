#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import pkg_resources

from ..util_core.loader import Loader
from ..util_core.utils import ColorStr, calcul_iptables_traffic

def manage():
    loader = Loader()

    profile = loader.profile

    group_list = profile.group_list

    while True:
        print("")
        print("Iptables 端口流量统计")
        print("")
        print("1.查看流量统计\n")
        print("2.重置流量统计\n")
        print("tip: v2ray功能端口默认自动开启iptables的流量统计\n")

        choice = input("请输入数字选择功能：")
        if choice == "1":
            print("")
            for group in group_list:
                print(calcul_iptables_traffic(group.port))
            print("")

        elif choice == "2":
            port = input("请输入要重置流量的端口：")
            if port and port.isnumeric():
                subprocess.call("bash {0} {1}".format(pkg_resources.resource_filename(__name__, "clean_traffic.sh"), str(port)), shell=True)
            else:
                print(ColorStr.red("输入有误!"))
        else:
            break