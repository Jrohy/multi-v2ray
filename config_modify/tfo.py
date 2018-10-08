#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from group import Mtproto, SS
from writer import GroupWriter
from selector import GroupSelector

gs = GroupSelector('修改tcpFastOpen')
group = gs.group

if group == None:
    exit(-1)
else:
    if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
        print("\nv2ray MTProto/Shadowsocks协议不支持配置tcpFastOpen!!!\n")
        exit(-1)
    
    print('当前组的tcpFastOpen状态：{}'.format(group.tfo))
    print("")
    print("1.开启TFO(强制开启)")
    print("2.关闭TFO(强制关闭)")
    print("3.删除TFO(使用系统默认设置)")
    choice = input("请输入数字选择功能：")
    
    gw = GroupWriter(group.tag, group.index)
    if choice == "1":
        gw.write_tfo('on')
    elif choice == "2":
        gw.write_tfo('off')
    elif choice == "3":
        gw.write_tfo('del')
    else:
        print("输入错误，请重试！")