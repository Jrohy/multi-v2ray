#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
from base_util import tool_box

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 1

if length > 1:
    import server_info
    choice=input("请输入要删除的user节点序号数字:")
    if not tool_box.is_number(choice):
        print("输入错误，请检查是否为数字")
        exit
    choice = int(choice)

if length==1 or (choice > 0 and choice <= len(mul_user_conf)):
    print("你选择的user信息:")
    print(mul_user_conf[choice - 1])
    schoice = input("是否删除y/n：")
    if schoice == 'y' or schoice == 'Y':
        write_json.del_user(choice - 1)
    else:
        print("撤销删除")
else:
    print ("输入错误，请检查是否符合范围中")