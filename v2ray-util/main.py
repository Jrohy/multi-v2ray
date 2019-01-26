#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

from .util_core.v2ray import V2ray
from .util_core.utils import ColorStr

def loop_input_choice_number(input_tip, number_max):
    """
    循环输入选择的序号,直到符合规定为止
    """
    while True:
        choice = input(input_tip)
        if not choice:
            sys.exit(0)
        if choice.isnumeric():
            choice = int(choice)
        else:
            print(ColorStr.red("输入有误,请重新输入"))
            continue
        if (choice <= number_max and choice > 0):
            return choice
        else:
            print(ColorStr.red("输入有误,请重新输入"))

def parse_command(quality, mode, path, thread, verbose, url):
    pass


def service_manage():
    show_text = ("启动服务", "停止服务", "重启服务", "运行状态")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("请选择: ", len(show_text))
    if choice == 1:
        V2ray.start()
    elif choice == 2:
        V2ray.stop()
    elif choice == 3:
        V2ray.restart()
    elif choice == 4:
        V2ray.status()

def user_manage():
    show_text = ("新增用户", "新增端口", "删除用户", "删除端口")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("请选择: ", len(show_text))
    if choice == 1:
        from .user_manage import create_new_user
    elif choice == 2:
        from .user_manage import create_new_port
    elif choice == 3:
        from .user_manage import del_user
    elif choice == 4:
        from .user_manage import del_port

def profile_alter():
    show_text = ("更改email", "更改UUID", "更改alterID", "更改主端口", "更改传输方式", "更改TLS设置", 
                "更改tcpFastOpen设置", "更改动态端口", "更改Shadowsocks加密方式", "更改Shadowsocks密码")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("请选择: ", len(show_text))
    if choice == 1:
        from .profile_alter import n_email
    elif choice == 2:
        from .profile_alter import n_uuid
    elif choice == 3:
        from .profile_alter import alterid
    elif choice == 4:
        from .profile_alter import port
    elif choice == 5:
        from .profile_alter import stream
    elif choice == 6:
        from .profile_alter import tls
    elif choice == 7:
        from .profile_alter import tfo
    elif choice == 8:
        from .profile_alter import dyn_port
    elif choice == 9:
        from .profile_alter import ss
    elif choice == 10:
        from .profile_alter import ss
    V2ray.restart()

def global_setting():
    show_text = ("流量统计(v2ray)", "流量统计(iptables)", "禁止bittorrent", "定时更新V2ray", "清理v2ray日志", "脚本升级")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("请选择: ", len(show_text))
    if choice == 1:
        from .global_setting import stats_ctr
    elif choice == 2:
        from .global_setting import iptables_ctr
    elif choice == 3:
        from .global_setting import ban_bt
    elif choice == 4:
        os.system("bash global_setting/update_timer.sh")
    elif choice == 5:
        V2ray.cleanLog()
    elif choice == 6:
        pass

def main_menu():
    while True:
        print("")
        print("欢迎使用 v2ray 管理程序")
        show_text = ("1.服务管理", "2.用户管理", "3.更改配置", "4.查看配置", "5.全局功能", "6.更新V2Ray", "7.生成客户端配置文件")
        for index, text in enumerate(show_text): 
            if index % 2 == 0:
                print('{:<25}'.format(text), end="")   
            else:
                print(text)
        choice = loop_input_choice_number("请选择: ", len(show_text))
        if choice == 1:
            service_manage()
        elif choice == 2:
            user_manage()
        elif choice == 3:
            profile_alter()
        elif choice == 4:
            from .util_core.loader import Loader 
            print(Loader().profile)
        elif choice == 5:
            global_setting()
        elif choice == 6:
            V2ray.update()
        elif choice == 6:
            from .util_core import client

if __name__ == "__main__":
    main_menu()