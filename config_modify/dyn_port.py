#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import read_json
import write_json
from base_util import v2ray_util

print("当前动态端口状态: %s\n") % str(read_json.conf_Dyp)

dp=input("是否开启动态端口(y/n)")

if dp == 'y' or dp == 'Y':
    newAlterId=input("请为动态端口设置alterID(默认32): ")
    if newAlterId == '':
        newAlterId='32'
    if (not v2ray_util.is_number(newAlterId)):
        print ("\n输入错误，请检查是否为数字")
    else:
        write_json.en_dyn_port(1, newAlterId)
        print("\n成功开启动态端口!")
elif dp == 'n' or dp == 'N':
    write_json.en_dyn_port(0)
    print("\n成功关闭动态端口!")
else:
    print ("\n输入错误，请检查重新输入")