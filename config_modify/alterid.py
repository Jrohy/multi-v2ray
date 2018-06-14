#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
from base_util import v2ray_util

mul_user_conf = read_json.multiUserConf

choice=input("请输入要改alterId的节点序号:")
if not v2ray_util.is_number(choice):
    print("输入错误，请检查是否为数字")
    exit
choice = int(choice)

if choice > 0 and choice <= len(mul_user_conf):
    new_alterid=input("请输入新的alterID: ")
    if (v2ray_util.is_number(new_alterid)):
        write_json.write_alterid(new_alterid, mul_user_conf[choice - 1]['indexDict'])
        print("alterID修改成功！")
    else:
        print ("输入错误，请检查是否为数字")
else:
    print ("输入错误，请检查是否符合范围中")