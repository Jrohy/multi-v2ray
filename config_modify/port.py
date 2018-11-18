#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from writer import GroupWriter
from selector import GroupSelector

gs = GroupSelector('修改port')
group = gs.group

if group == None:
    exit(-1)
else:
    if group.end_port:
        port_info = "{0}-{1} {2}".format(group.port, group.end_port, group.port_strategy)
    else:
        port_info = group.port
    print('当前组的端口信息为：{}'.format(port_info))

    port_strategy="always"
    new_port_info = input("请输入新端口(单端口直接数字, 端口范围用'-'隔开)：")
    if new_port_info.find("-") > 0:
        print("是否开启随机分配监听端口(random), 否则监听全部范围端口(always)")
        choice = input("请选择(是输入y, 否直接回车)：")
        if choice == 'y':
            print("random模式监听端口")
            port_strategy="random"
        else:
            print("always模式监听端口")
    gw = GroupWriter(group.tag, group.index)
    gw.write_port(new_port_info, port_strategy)
    print('端口修改成功！')