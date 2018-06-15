#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
from base_util import v2ray_util

mul_user_conf = read_json.multiUserConf
choice=input("请输入要删除的user节点序号:")
if not v2ray_util.is_number(choice):
    print("输入错误，请检查是否为数字")
    exit
choice = int(choice)

if choice > 0 and choice <= len(mul_user_conf):
    print("你选择的user信息:")
    print(mul_user_conf[choice - 1])
    schoice = input("是否删除y/n：")
    if schoice == 'y':
        write_json.del_user(choice - 1)
    else:
        print("撤销删除")
else:
    print ("输入错误，请检查是否符合范围中")