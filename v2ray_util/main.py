#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import pkg_resources

from .util_core.v2ray import V2ray
from .util_core.utils import ColorStr, open_port
from .global_setting import stats_ctr, iptables_ctr, ban_bt
from .config_modify import base, multiple, ss, stream, tls

def loop_input_choice_number(input_tip, number_max):
    """
    循环输入选择的序号,直到符合规定为止
    """
    while True:
        print("")
        choice = input(input_tip)
        if not choice:
            break
        if choice.isnumeric():
            choice = int(choice)
        else:
            print(ColorStr.red("输入有误,请重新输入"))
            continue
        if (choice <= number_max and choice > 0):
            return choice
        else:
            print(ColorStr.red("输入有误,请重新输入"))

def help():
    print("""
v2ray [-h|--help] [-v|--version] [options]
    -h, --help           查看帮助
    -v, --version        查看版本信息
    start                启动 V2Ray
    stop                 停止 V2Ray
    restart              重启 V2Ray
    status               查看 V2Ray 运行状态
    new                  新建全新配置
    update               更新 V2Ray 到最新Release版本
    update [version]     更新 V2Ray 到特定版本
    update.sh            更新 multi-v2ray
    update.sh [version]  更新 multi-v2ray 到特定版本
    add                  新增mkcp + 随机一种 (srtp | wechat-video | utp | dtls) header伪装的端口(Group)
    add [wechat|utp|srtp|dtls|wireguard|socks|mtproto|ss]     新增一种协议的组，端口随机,如 v2ray add utp 为新增utp协议
    del                  删除端口组
    info                 查看配置
    port                 修改端口
    tls                  修改tls
    tfo                  修改tcpFastOpen
    stream               修改传输协议
    stats                iptables流量统计
    clean                清理日志
    更多功能 请输入 v2ray 回车进入服务管理程序
    """)

def parse_arg():
    if len(sys.argv) == 1:
        return
    elif len(sys.argv) == 2:
        if sys.argv[1] == "start":
            V2ray.start()
        elif sys.argv[1] == "stop":
            V2ray.stop()
        elif sys.argv[1] == "restart":
            V2ray.restart()
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            help()
        elif sys.argv[1] == "status":
            V2ray.status()
        elif sys.argv[1] == "info":
            V2ray.info()
        elif sys.argv[1] == "port":
            base.port()
            open_port()
            V2ray.restart()
        elif sys.argv[1] == "tls":
            tls.modify()
            V2ray.restart()
        elif sys.argv[1] == "tfo":
            base.tfo()
            V2ray.restart()
        elif sys.argv[1] == "stream":
            stream.modify()
            V2ray.restart()
        elif sys.argv[1] == "stats":
            iptables_ctr.manage()
        elif sys.argv[1] == "clean":
            V2ray.cleanLog()
        elif sys.argv[1] == "del":
            multiple.del_port()
            V2ray.restart()
        elif sys.argv[1] == "add":
            multiple.new_port()
            V2ray.restart()
        elif sys.argv[1] == "update":
            V2ray.update()
        elif sys.argv[1] == "new":
            V2ray.new()
    else:
        if sys.argv[1] == "add":
            multiple.new_port(sys.argv[2])
            V2ray.restart()
    sys.exit(0)

def service_manage():
    show_text = ("启动服务", "停止服务", "重启服务", "运行状态")
    print("")
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
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("请选择: ", len(show_text))
    if choice == 1:
        multiple.new_user()
    elif choice == 2:
        multiple.new_port()
    elif choice == 3:
        multiple.del_user()
    elif choice == 4:
        multiple.del_port()
    V2ray.restart()

def profile_alter():
    show_text = ("更改email", "更改UUID", "更改alterID", "更改主端口", "更改传输方式", "更改TLS设置", 
                "更改tcpFastOpen设置", "更改动态端口", "更改Shadowsocks加密方式", "更改Shadowsocks密码")
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("请选择: ", len(show_text))
    if choice == 1:
        base.new_email()
    elif choice == 2:
        base.new_uuid()
    elif choice == 3:
        base.alterid()
    elif choice == 4:
        base.port()
    elif choice == 5:
        stream.modify()
    elif choice == 6:
        tls.modify()
    elif choice == 7:
        base.tfo()
    elif choice == 8:
        base.dyn_port()
    elif choice == 9:
        ss.modify('method')
    elif choice == 10:
        ss.modify('password')
    V2ray.restart()

def global_setting():
    show_text = ("流量统计(v2ray)", "流量统计(iptables)", "禁止bittorrent", "定时更新V2ray", "清理v2ray日志", "脚本升级")
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("请选择: ", len(show_text))
    if choice == 1:
        stats_ctr.manage()
    elif choice == 2:
        iptables_ctr.manage()
    elif choice == 3:
        ban_bt.manage()
    elif choice == 4:
        subprocess.call("bash {0}".format(pkg_resources.resource_filename(__name__, "global_setting/update_timer.sh")), shell=True)
    elif choice == 5:
        V2ray.cleanLog()
    elif choice == 6:
        V2ray.update()

def menu():
    V2ray.check()
    parse_arg()
    while True:
        print("")
        print(ColorStr.cyan("欢迎使用 v2ray 管理程序"))
        print("")
        show_text = ("1.服务管理", "2.用户管理", "3.更改配置", "4.查看配置", "5.全局功能", "6.更新V2Ray", "7.生成客户端配置文件")
        for index, text in enumerate(show_text): 
            if index % 2 == 0:
                print('{:<20}'.format(text), end="")   
            else:
                print(text)
                print("")
        print("")
        choice = loop_input_choice_number("请选择: ", len(show_text))
        if choice == 1:
            service_manage()
        elif choice == 2:
            user_manage()
        elif choice == 3:
            profile_alter()
        elif choice == 4:
            V2ray.info()
        elif choice == 5:
            global_setting()
        elif choice == 6:
            V2ray.update()
        elif choice == 7:
            from .util_core import client
            client.generate()
        else:
            break

if __name__ == "__main__":
    menu()