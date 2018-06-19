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
    choice=input("请输入要改alterId的节点序号数字:")
    if not tool_box.is_number(choice):
        print("输入错误，请检查是否为数字")
        exit
    choice = int(choice)

if length == 1 or (choice > 0 and choice <= length):
    new_alterid=input("请输入新的alterID: ")
    if (tool_box.is_number(new_alterid)):
        write_json.write_alterid(new_alterid, mul_user_conf[choice - 1]['indexDict'])
        print("alterID修改成功！")
    else:
        print ("输入错误，请检查是否为数字")
else:
    print ("输入错误，请检查是否符合范围中")