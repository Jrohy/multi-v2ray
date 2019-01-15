#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

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

def main_menu():
    print("")
    print("欢迎使用 v2ray-util 管理程序")
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


    
if __name__ == "__main__":
    main_menu()