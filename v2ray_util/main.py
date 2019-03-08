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
            print(ColorStr.red("input error, please input again"))
            continue
        if (choice <= number_max and choice > 0):
            return choice
        else:
            print(ColorStr.red("input error, please input again"))

def help():
    exec_name = sys.argv[0]
    print("""
{0} [-h|--help] [options]
    -h, --help           get help
    start                start V2Ray
    stop                 stop V2Ray
    restart              restart V2Ray
    status               check V2Ray status
    new                  create new json profile
    update               update v2ray to latest
    add                  random create mkcp + (srtp | wechat-video | utp | dtls) fake header group
    add [wechat|utp|srtp|dtls|wireguard|socks|mtproto|ss]     create special protocol, random new port
    del                  delete port group
    info                 check v2ray profile
    port                 modify port
    tls                  modify tls
    tfo                  modify tcpFastOpen
    stream               modify protocol
    stats                iptables traffic statistics
    clean                clean v2ray log
    """.format(exec_name[exec_name.rfind("/") + 1:]))

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
            open_port()
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
    show_text = ("start v2ray", "stop v2ray", "restart v2ray", "v2ray status")
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("please select: ", len(show_text))
    if choice == 1:
        V2ray.start()
    elif choice == 2:
        V2ray.stop()
    elif choice == 3:
        V2ray.restart()
    elif choice == 4:
        V2ray.status()

def user_manage():
    show_text = ("add user", "add port", "del user", "del port")
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("please select: ", len(show_text))
    if choice == 1:
        multiple.new_user()
    elif choice == 2:
        multiple.new_port()
        open_port()
    elif choice == 3:
        multiple.del_user()
    elif choice == 4:
        multiple.del_port()
    V2ray.restart()

def profile_alter():
    show_text = ("email", "UUID", "alterID", "port", "stream", "tls",
                "tcpFastOpen", "dyn_port", "shadowsocks method", "shadowsocks password")
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("please select: ", len(show_text))
    if choice == 1:
        base.new_email()
    elif choice == 2:
        base.new_uuid()
    elif choice == 3:
        base.alterid()
    elif choice == 4:
        base.port()
        open_port()
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
    show_text = ("V2ray Traffic Statistics", "Iptables Traffic Statistics", "Ban Bittorrent", "Schedule Update V2ray", "Clean Log")
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number("please select: ", len(show_text))
    if choice == 1:
        stats_ctr.manage()
    elif choice == 2:
        iptables_ctr.manage()
    elif choice == 3:
        ban_bt.manage()
        V2ray.restart()
    elif choice == 4:
        subprocess.call("bash {0}".format(pkg_resources.resource_filename(__name__, "global_setting/update_timer.sh")), shell=True)
    elif choice == 5:
        V2ray.cleanLog()

def menu():

    from .manager import Managecmd

    mgcmd = Managecmd()
    mgcmd.cmdloop()
    return

    V2ray.check()
    parse_arg()
    while True:
        print("")
        print(ColorStr.cyan("Welcome to v2ray-util"))
        print("")
        show_text = ("1.V2ray Manage", "2.Group Manage", "3.Modify Config", "4.Check Config", "5.Global Setting", "6.Update V2Ray", "7.Generate Client Json")
        for index, text in enumerate(show_text):
            if index % 2 == 0:
                print('{:<20}'.format(text), end="")
            else:
                print(text)
                print("")
        print("")
        choice = loop_input_choice_number("please select: ", len(show_text))
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
