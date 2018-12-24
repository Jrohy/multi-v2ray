#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from writer import GroupWriter
from selector import GroupSelector

gs = GroupSelector('修改动态端口')
group = gs.group

if group == None:
    pass
else:
    print('当前组的动态端口状态：{}'.format(group.dyp))
    gw = GroupWriter(group.tag, group.index)
    
    choice = input("是否开启动态端口(y/n): ").lower()

    if choice == 'y':
        newAlterId = input("请为动态端口设置alterID(默认32): ")
        newAlterId = '32' if newAlterId == '' else newAlterId
        if (newAlterId.isdecimal()):
            gw.write_dyp(True, newAlterId)
            print("\n成功开启动态端口!")
        else:
            print ("\n输入错误，请检查是否为数字")
    elif choice == 'n':
        gw.write_dyp(False)
        print("\n成功关闭动态端口!")
    else:
        print ("\n输入错误，请检查重新输入")