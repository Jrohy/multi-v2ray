#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson
from v2rayutil import is_number

print("当前动态端口状态: %s\n") % str(readjson.ConfDyp)

dp=raw_input("是否开启动态端口(y/n)")

if dp == 'y' or dp == 'Y':
    newAlterId=raw_input("请为动态端口设置alterID(默认32): ")
    if newAlterId == '':
        newAlterId='32'
    if (not is_number(newAlterId)):
        print ("\n输入错误，请检查是否为数字")
    else:
        writejson.EnDynPort(1, newAlterId)
        print("\n成功开启动态端口!")
elif dp == 'n' or dp == 'N':
    writejson.EnDynPort(0)
    print("\n成功关闭动态端口!")
else:
    print ("\n输入错误，请检查重新输入")