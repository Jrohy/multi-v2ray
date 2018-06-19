#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
import re
from base_util import tool_box

mul_user_conf = read_json.multiUserConf

length = len(mul_user_conf)

choice = 'A'

if length > 1:
    import server_info
    choice=input("请输入要改动态端口的节点Group字母:")
    choice=choice.upper()

if length == 1 or (len(choice)==1 and re.match(r'[A-Z]', choice) and choice <= mul_user_conf[-1]['indexDict']['group']):

    for sin_user_conf in mul_user_conf:
        if sin_user_conf['indexDict']['group'] == choice:
            index_dict = sin_user_conf['indexDict']
            print ("当前组动态端口状态：%s\n" % str(sin_user_conf['dyp'])) 
            break

    dp=input("是否开启动态端口(y/n)")

    if dp == 'y' or dp == 'Y':
        newAlterId=input("请为动态端口设置alterID(默认32): ")
        if newAlterId == '':
            newAlterId='32'
        if (not tool_box.is_number(newAlterId)):
            print ("\n输入错误，请检查是否为数字")
        else:
            write_json.en_dyn_port(1, index_dict, newAlterId)
            print("\n成功开启动态端口!")
    elif dp == 'n' or dp == 'N':
        write_json.en_dyn_port(0, index_dict)
        print("\n成功关闭动态端口!")
    else:
        print ("\n输入错误，请检查重新输入")
else:
    print("输入有误，请检查是否为字母且范围中")
