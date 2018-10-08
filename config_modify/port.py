#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from writer import GroupWriter
from selector import GroupSelector

gs = GroupSelector('修改port')
group = gs.group

if group == None:
    exit(-1)
else:
    print('当前组的端口为：{}'.format(group.port))
    new_port = input("请输入新端口：")
    if (new_port.isdecimal()):
        gw = GroupWriter(group.tag, group.index)
        gw.write_port(new_port)
        print('端口修改成功！')
    else:
        print("输入错误，请检查是否为数字")